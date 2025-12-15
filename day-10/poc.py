#!/bin/env python3.14t


from fractions import Fraction
from itertools import product
from math import inf, lcm
from operator import itemgetter
from sys import argv


def analyze(_, buttons, joltages):
	try:
		print()

		matrix = [[Fraction(1) if i in b else Fraction(0) for i in range(len(joltages))] for b in buttons]
		matrix = transpose(matrix)
		matrix = [(*mr, Fraction(r)) for (mr, r) in zip(matrix, joltages)]

		bounds = get_bounds(matrix)

		solutions = solve(matrix, bounds)

		for index in range(len(solutions)):
			multiplier = lcm(*(s.denominator for s in solutions[index] if s))

			solutions[index] = (s * multiplier for s in solutions[index])
			solutions[index] = tuple(s.numerator if s.is_integer() else s for s in solutions[index])

		for index in range(len(matrix)):
			multiplier = lcm(*(c.denominator for c in matrix[index] if c))

			matrix[index] = (c * multiplier for c in matrix[index])
			matrix[index] = tuple(c.numerator if c.is_integer() else c for c in matrix[index])

		print(*matrix, sep='\n', end='\n\n')
		print(*bounds, end='\n\n')
		print(*solutions, sep='\n')

		return min((sum(s) for s in solutions), default=0)
	finally:
		print()


def count(iterable):
	result = 0

	for _ in iterable:
		result += 1

	return result


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


def get_equations(matrix, results):
	def get_check(variables, result):
		def check(coefficients):
			return sum((c * v for (c, v) in zip(coefficients, variables))) == result

		return check

	return [get_check(r[:-1], r[-1]) for r in matrix]


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


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


def reduce(matrix):
	"""
	Reduce the linear system matrix into row echelon form via Gaussian elimination.

	By doing this for all lines and not just lower ones I'm eliminationg front variables at the same time from every equation.
	From my testing this seems to reduce the equations into a from that do not share subsets of variables.
	The end result is filtered and only non-trivial rows are returned.
	"""

	matrix = list(matrix)

	index_row = 0

	while index_row < len(matrix):
		try:
			matrix[index_row:] = sorted(matrix[index_row:], key=lambda mr: min((i for (i, mc) in enumerate(mr) if mc), default=inf))

			row_current = matrix[index_row]
			index_column = min((i for (i, cc) in enumerate(row_current) if cc), default=-1)

			if index_column == -1:
				continue

			column_current = row_current[index_column]
			matrix[index_row] = row_current = tuple(c / column_current for c in row_current)

			for index in range(len(matrix)):
				if index_row == index:
					continue

				row = matrix[index]

				multiplier = row[index_column]

				if not multiplier:
					continue

				matrix[index] = tuple(c - multiplier * cc for (c, cc) in zip(row, row_current))
		finally:
			index_row += 1

	matrix = [r for r in matrix if any(r)]

	return matrix

def solve(matrix, bounds):
	if not len(matrix):
		return []

	solutions = set()

	def solve_internal(matrix_initial, solution_initial):
		matrix = reduce(matrix_initial)

		if any(not any(r[:-1]) and r[-1] for r in matrix):
			return

		solution = list(solution_initial)

		substitutions = ((i, r) for (i, r) in enumerate(matrix) if count(c for c in r[:-1] if c) == 1)
		substitutions = sorted(substitutions, key=itemgetter(0), reverse=True)

		for (index_row, row) in substitutions:
			index_variable = min((i for (i, r) in enumerate(row) if r))

			if not (solution[index_variable] is None or solution[index_variable] == row[-1]):
				raise ValueError(f'Solution already has a value; index: {index_variable}, current: {solution[index_variable]}, candidate: {row[-1]}.')

			solution[index_variable] = row[-1]

			del matrix[index_row]

		if not all(s is None or (s.is_integer() and l <= s <= u) for (s, (l, u)) in zip(solution, bounds)):
			return

		solution = tuple(solution)

		if not (any(s is None for s in solution) or solution in solutions):
			solutions.add(solution)

			yield solution

		if not len(matrix):
			return

		for (index, (lower, upper)) in enumerate(bounds):
			if solution[index] is not None:
				continue

			for guess_variable in range(lower, upper + 1):
				guess_solution = tuple(guess_variable if i == index else s for (i, s) in enumerate(solution))

				if guess_solution in solutions:
					continue

				solutions.add(guess_solution)

				guess_matrix = list((*(0 if i == index else c for (i, c) in enumerate(r[:-1])), r[-1] - r[index] * guess_variable) for r in matrix)

				yield from solve_internal(guess_matrix, guess_solution)

	return list(solve_internal(matrix, (None for _ in bounds)))


def transpose(matrix):
	def transpose_column(column):
		for row in range(len(matrix)):
			yield matrix[row][column]

	def transpose_rows():
		for column in range(len(matrix[0])):
			yield list(transpose_column(column))

	return list(transpose_rows())


if __name__ == '__main__':
	main()
