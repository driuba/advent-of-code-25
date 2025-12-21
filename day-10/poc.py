#!/bin/env python3.14t


from fractions import Fraction
from itertools import product
from math import inf, lcm
from operator import itemgetter
from sys import argv

from matrices import (
	add_member,
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

		solution = solve(matrix, [[Fraction(1)] for _ in matrix[0][:-1]])

		solution = [s.numerator if s.is_integer() else s for s in solution]

		for index in range(len(matrix)):
			multiplier = lcm(*(c.denominator for c in matrix[index] if c))

			matrix[index] = (c * multiplier for c in matrix[index])
			matrix[index] = [c.numerator if c.is_integer() else c for c in matrix[index]]

		print(*matrix, sep='\n', end='\n\n')
		print(*solution)

		return sum(solution)
	except NotImplementedError:
		return 0
	finally:
		print()


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

	def __construct_inverse(matrix_transposed, indices_basic):
		matrix_basic = transpose([matrix_transposed[i] for i in indices_basic])

		matrix_basic_inverse = [[*rb, *ri] for (rb, ri) in zip(matrix_basic, identity(len(matrix_basic), Fraction))]
		matrix_basic_inverse = reduce(matrix_basic_inverse)
		matrix_basic_inverse = [r[len(r) // 2:] for r in matrix_basic_inverse]

		return matrix_basic_inverse

	indices_basic = []

	for row in matrix:
		for (index, column) in enumerate(row[:-1]):
			if not column:
				continue

			if index in indices_basic:
				continue

			indices_basic.append(index)

			break

	matrix_transposed = transpose(matrix)

	matrix_basic_inverse = __construct_inverse(matrix_transposed, indices_basic)

	solution = [[Fraction(0)] for _ in matrix[0][:-1]]

	solution_basic = multiply(matrix_basic_inverse, [[r[-1]] for r in matrix])

	for (index_solution, solution_variable) in zip(indices_basic, solution_basic):
		solution[index_solution] = solution_variable

	while True:
		solution_basic = multiply(matrix_basic_inverse, [[r[-1]] for r in matrix])

		target_basic = [target[ib] for ib in indices_basic]

		costs = multiply_member(target, solution)

		costs_basic = transpose(multiply_member(target_basic, solution_basic))

		(index_entering, cost_entering, distances_basic) = min(
			(
				(
					i,
					costs[i][0] - multiply(costs_basic, d)[0][0],
					d
				)
				for (i, d)
				in (
					(i, multiply(matrix_basic_inverse, transpose([r])))
					for (i, r)
					in enumerate(matrix_transposed[:-1])
					if i not in indices_basic
				)
			),
			key=itemgetter(1)
		)

		if cost_entering >= 0:
			return transpose(solution)[0]

		(index_leaving, distance_leaving, ratio) = min(
			(
				(i, db, sb / -db if db else sb * inf)
				for (i, (sb, db))
				in enumerate(zip(
					transpose(solution_basic)[0],
					transpose(distances_basic)[0]
				))
			),
			key=itemgetter(1)
		)

		if distance_leaving >= 0:
			return []

		distances = [[Fraction(0)] for _ in solution]

		for (index_basic, distance_basic) in zip(indices_basic, distances_basic):
			distances[index_basic] = distance_basic

		distances[index_entering] = [Fraction(1)]

		distances = multiply_scalar(ratio, distances)

		solution = add_member(solution, distances)

		indices_basic[index_leaving] = index_entering

		matrix_basic_inverse = [
			r[1:]
			for r
			in reduce([[*d, *r] for (d, r) in zip(distances_basic, matrix_basic_inverse)], index_leaving)
		]


def process(filename):
	machines = read_file(filename)

	total = 0

	for machine in machines:
		result = analyze(*machine)

		total += result

		print('The result is', result)

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

	matrix = [r.copy() for r in matrix]

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

def solve(matrix, target):
	if not len(matrix):
		return []

	matrix = reduce(matrix)

	if any((all((not c for c in r[:-1])) and r[-1] for r in matrix)):
		return []

	if all((sum((1 for c in r[:-1] if c)) == 1 for r in matrix)):
		return [r[-1] for r in matrix]

	return optimize(matrix, target)


if __name__ == '__main__':
	main()
