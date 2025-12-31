#!/bin/env python3.14t


from collections import deque
from fractions import Fraction
from itertools import product
from math import (
	ceil,
	floor,
	inf,
	lcm
)
from operator import itemgetter
from sys import argv

import numpy as np
from scipy.optimize import linprog

from matrices import (
	add_member,
	copy,
	identity,
	multiply,
	multiply_member,
	multiply_scalar,
	transpose
)


def analyze(_, buttons, joltages):
	try:
		print()

		matrix = [[Fraction(1) if i in b else Fraction(0) for i in range(len(joltages))] for b in buttons]
		matrix = transpose(matrix)
		matrix = [[*mr, Fraction(r)] for (mr, r) in zip(matrix, joltages)]

		matrix_np = np.matrix(matrix, dtype=float)

		c = np.ones(matrix_np.shape[1] - 1, dtype=float)
		A = matrix_np[:, :-1]
		b = matrix_np[:, -1].T[0]
		bounds = [(0, None)] * (matrix_np.shape[1] - 1)

		solution_sp = linprog(c, A_eq=A, b_eq=b, integrality=1)
		solution_sp = np.rint(solution_sp.x).astype(int)

		result_sp = solution_sp.sum()

		solution = solve(matrix, [[Fraction(1)] for _ in matrix[0][:-1]], get_bounds(matrix))

		result = sum(solution)

		# [validation] = (A @ np.matrix([solution], dtype=float).T).T
		# [validation_sp] = (A @ solution_sp.reshape((-1, 1))).T
		#
		# print(validation)
		# print(validation_sp)

		for row in matrix:
			for column in row:
				print(f'{column: >8}', end='')

			print()

		print()

		for variable in solution:
			print(' ' * 8 if variable is None else f'{variable: >8}', end='')

		print()

		for variable in solution_sp:
			print(' ' * 8 if variable is None else f'{variable: >8}', end='')

		print()

		print(result, result_sp)

		if result != result_sp:
			raise Exception('This matrix right here, officer.')

		return result
	finally:
		print()


def get_bounds(matrix):
	"""
	Computes bounds from **initial** equation system matrix.

	Initial implies variables being integers in range [0:1] and results column containing only non-negative integers.
	All matrix values are expected to be of `Fraction` type.
	"""

	upper = [
		min((c.numerator for c in r if c), default=0)
		for r in transpose([
			[r[-1] if c else 0 for c in r[:-1]]
			for r in matrix
		])
	]

	lower = [0 for _ in upper]

	for row in matrix:
		value = row[-1].numerator

		row = [c.numerator * u for (c, u) in zip(row, upper)]

		for (index, lower_current) in enumerate(lower):
			if not row[index]:
				continue

			lower[index] = max(lower_current, value - sum(b for (i, b) in enumerate(row) if i != index))

	lower = (min(l, u) for (l, u) in zip(lower, upper))

	return list(zip(lower, upper))


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def optimize(matrix, target):
	"""
	Simplex optimization to find optimal solution.

	This method is supposed to be used if the system has infinite amount of solutions.
	However, it should work in cases where there's only one solution.
	The input is expected to be normal linear equation system in matrix form.
	"""

	matrix = copy(matrix)
	matrix_basic_inverse = identity(len(matrix), Fraction)

	for (index, row) in enumerate(matrix):
		if row[-1] < 0:
			matrix[index] = [-1 * c for c in row]

			row = matrix[index]

		matrix[index] = row[:-1] + matrix_basic_inverse[index] + row[-1:]

	matrix_transposed = transpose(matrix)

	target_phase_1 = [[Fraction(0)] for _ in target] + [[Fraction(1)] for _ in matrix]
	target_phase_2 = target

	target = target_phase_1

	count_variables = len(target) - len(matrix)

	solution = [[Fraction(0)] for i in range(count_variables)]
	solution += [r[-1:] for r in matrix]

	indices_basic = list(range(count_variables, len(target)))

	# print(*(f'{i: >8}' for i in indices_basic), sep='')
	# print(*(f'{s[0]: >8}' for s in solution), sep='')
	# print(*(f'{t[0]: >8}' for t in target), sep='', end='\n\n')

	# for row in matrix:
	# 	for column in row:
	# 		print(f'{column: >8}', end='')
	#
	# 	print()
	#
	# print()

	while True:
		solution_basic = multiply(matrix_basic_inverse, [r[-1:] for r in matrix])

		target_basic = transpose([target[ib] for ib in indices_basic])

		# print(*(f'{i: >8}' for i in indices_basic), sep='')
		# print(*(f'{s[0]: >8}' for s in solution_basic), sep='')
		# print(*(f'{s[0]: >8}' for s in solution), sep='')
		# print(*(f'{c: >8}' for c in target_basic[0]), sep='', end='\n\n')

		# print(
		# 	*(
		# 		(i, c)
		# 		for (i, c, d)
		# 		in (
		# 			(
		# 				i,
		# 				target[i][0] - multiply(target_basic, d)[0][0],
		# 				d
		# 			)
		# 			for (i, d)
		# 			in (
		# 				(i, multiply(matrix_basic_inverse, transpose([r])))
		# 				for (i, r)
		# 				in enumerate(matrix_transposed[:-1])
		# 				if i not in indices_basic
		# 			)
		# 		)
		# 	),
		# 	sep='\n'
		# )

		(index_entering, cost_entering, distances_basic) = min(
			(
				(i, c, d)
				for (i, c, d)
				in (
					(
						i,
						target[i][0] - multiply(target_basic, d)[0][0],
						d
					)
					for (i, d)
					in (
						(i, multiply(matrix_basic_inverse, transpose([r])))
						for (i, r)
						in enumerate(matrix_transposed[:-1])
						if i not in indices_basic
					)
				)
				if c < 0
			),
			default=(None, 0, None),
			key=itemgetter(1, 0)
		)

		# print(index_entering, cost_entering, distances_basic, end='\n\n')

		if index_entering is None:
			if any((s for [s] in solution[count_variables:])):
				return []

			return transpose(solution)[0]

		# print(
		# 	*(
		# 		(i, sb, db)
		# 		for (i, (sb, db))
		# 		in enumerate(zip(
		# 			transpose(solution_basic)[0],
		# 			transpose(distances_basic)[0]
		# 		))
		# 	),
		# 	sep='\n'
		# )

		(index_leaving, distance_leaving, ratio) = min(
			(
				(i, db, r)
				for (i, db, r, ib)
				in (
					(i, db, sb / db, ib)
					for (i, (sb, db, ib))
					in enumerate(zip(
						transpose(solution_basic)[0],
						transpose(distances_basic)[0],
						indices_basic
					))
					if db > 0
				)
				if r >= 0
			),
			default=(None, 0, None),
			key=itemgetter(2, 0)
		)

		if index_leaving is None:
			return []

		# print(index_leaving, distance_leaving, ratio, end='\n\n')

		for (index_basic, [distance_basic]) in zip(indices_basic, distances_basic):
			if index_basic == indices_basic[index_leaving]:
				solution[index_basic] = [Fraction(0)]
			else:
				solution[index_basic][0] -= ratio * distance_basic

		solution[index_entering] = [ratio]

		indices_basic[index_leaving] = index_entering

		matrix_basic_inverse = [
			r[1:]
			for r
			in reduce([[*d, *r] for (d, r) in zip(distances_basic, matrix_basic_inverse)], index_leaving)
		]

		if target is target_phase_1 and all((ib < count_variables for ib in indices_basic)):
			if any((s for [s] in solution[count_variables:])):
				return []

			matrix_transposed = matrix_transposed[:count_variables] + matrix_transposed[-1:]
			matrix = transpose(matrix_transposed)
			solution = solution[:count_variables]
			target = target_phase_2

		# print(index_entering, index_leaving, end='\n\n')

		# print(*(f'{i: >8}' for i in indices_basic), sep='', end='\n\n')
		#
		# for row in matrix_basic_inverse:
		# 	for column in row:
		# 		print(f'{column: >8}', end='')
		#
		# 	print()
		#
		# print()


def process(filename):
	machines = read_file(filename)

	total = 0

	for (index, machine) in enumerate(machines):
		result = analyze(*machine)

		total += result

		print('The result for', index + 1 ,'is', result)

	print('The total is', total)


def read_file(filename):
	def iterate():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				[state, *buttons, joltage] = line.split()

				state = state.strip('[]')
				buttons = (b.strip('()') for b in buttons)
				joltage = joltage.strip('{}')

				yield (
					tuple(s == '#' for s in state),
					[frozenset(int(l) for l in b.split(',')) for b in buttons],
					tuple(int(j) for j in joltage.split(','))
				)

	return list(iterate())


def reduce(matrix, index_row_target = None):
	"""
	Reduce the linear system matrix into row echelon form via Gauss-Jordan elimination.

	By doing this for all lines and not just lower ones I'm eliminationg front variables at the same time from every equation.
	From my testing this seems to reduce the equations into a from that do not share subsets of variables.
	The end result is filtered and only non-trivial rows are returned.
	"""

	matrix = copy(matrix)

	index_row = 0 if index_row_target is None else index_row_target
	count_rows = len(matrix) if index_row_target is None else index_row_target + 1

	while index_row < count_rows:
		try:
			if index_row_target is None:
				matrix[index_row:] = sorted(matrix[index_row:], key=lambda mr: next((i for (i, mc) in enumerate(mr) if mc), inf))

			row_current = matrix[index_row]
			index_column = next((i for (i, cc) in enumerate(row_current) if cc), -1) if index_row_target is None else 0

			if index_column == -1:
				continue

			column_current = row_current[index_column]
			matrix[index_row] = row_current = [c / column_current for c in row_current]

			for index in range(len(matrix)):
				if index_row == index:
					continue

				row = matrix[index]

				multiplier = row[index_column]

				if not multiplier:
					continue

				matrix[index] = [c - multiplier * cc for (c, cc) in zip(row, row_current)]
		finally:
			index_row += 1

	matrix = [r for r in matrix if any(r)]

	return matrix

def solve(matrix, target, bounds):
	def solve_internal(matrix, target):
		if not len(matrix):
			return []

		count_variables = len(matrix[0]) - 1

		matrix = reduce(matrix)

		# for row in matrix:
		# 	for column in row:
		# 		print(f'{column: >8}', end='')
		#
		# 	print()
		#
		# print()

		if any((all((not c for c in r[:-1])) and r[-1] for r in matrix)):
			return []

		target = copy(target)

		solution = {
			next((i for (i, c) in enumerate(r[:-1]) if c)): r[-1]
			for r in matrix
			if sum((1 for c in r[:-1] if c)) == 1
		}

		matrix = transpose(matrix)

		for index in sorted(solution, reverse=True):
			del matrix[index]
			del target[index]

		matrix = transpose(matrix)

		for index in range(len(matrix) - 1, -1, -1):
			if not any(matrix[index][:-1]):
				del matrix[index]

		solution = [
			solution[i] if i in solution else None
			for i in range(count_variables)
		]

		# for row in matrix:
		# 	for column in row:
		# 		print(f'{column: >8}', end='')
		#
		# 	print()
		#
		# print()
		#
		# for variable in solution:
		# 	print(' ' * 8 if variable is None else f'{variable: >8}', end='')
		#
		# print('\n')

		if not matrix:
			if all((s.is_integer() for s in solution)):
				return solution
			else:
				return []

		solution_optimized = optimize(matrix, target)

		if solution_optimized:
			index_optimized = 0

			for (index, variable) in enumerate(solution):
				if variable is None:
					solution[index] = solution_optimized[index_optimized]

					index_optimized += 1

		return solution

	queue = deque()

	queue.append(matrix)

	upper_bound = inf
	solution = []

	while queue:
		matrix = queue.popleft()

		candidate = solve_internal(matrix, target)

		if not candidate:
			continue

		if any((c is None for c in candidate)):
			continue

		if not all((l <= c <= u for (c, (l, u)) in zip(candidate, bounds))):
			continue

		[[cost]] = multiply([candidate], target)

		if upper_bound > cost:
			if all((c.is_integer() for c in candidate)):
				solution = candidate
				upper_bound = cost
			else:
				for (index, (variable, (lower, upper))) in enumerate(zip(candidate, bounds)):
					if variable.is_integer():
						continue

					for variable in [Fraction(floor(variable)), Fraction(ceil(variable))]:
						if lower <= variable <= upper:
							branch = copy(matrix)

							branch.append([*(Fraction(1) if i == index else Fraction(0) for i in range(len(candidate))), variable])

							queue.append(branch)

	return solution


if __name__ == '__main__':
	main()
