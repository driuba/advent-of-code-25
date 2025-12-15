#!/bin/env python3.14t


from fractions import Fraction
from itertools import product
from math import inf, lcm
from operator import itemgetter
from sys import argv


def analyze(_, buttons, joltages):
	try:
		matrix = [[Fraction(1) if i in b else Fraction(0) for i in range(len(joltages))] for b in buttons]
		matrix = transpose(matrix)
		matrix = [(*mr, Fraction(r)) for (mr, r) in zip(matrix, joltages)]

		solutions = solve(matrix)

		for index in range(len(solutions)):
			multiplier = lcm(*(s.denominator for s in solutions[index] if s))

			solutions[index] = (s * multiplier for s in solutions[index])
			solutions[index] = tuple(s.numerator if s.is_integer() else s for s in solutions[index])

		for index in range(len(matrix)):
			multiplier = lcm(*(c.denominator for c in matrix[index] if c))

			matrix[index] = (c * multiplier for c in matrix[index])
			matrix[index] = tuple(c.numerator if c.is_integer() else c for c in matrix[index])

		print(*matrix, sep='\n', end='\n\n')
		print(*solutions, sep='\n', end='\n\n')

		print(min(sum(s) for s in solutions))
	finally:
		print()


def count(iterable):
	result = 0

	for _ in iterable:
		result += 1

	return result


def get_bounds(matrix):
	bounds = transpose([[r[-1] / c if c else 0 for c in r[:-1]] for r in matrix])

	return [min((c for c in r if c > 0), default=0) for r in bounds]


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

	for machine in machines:
		analyze(*machine)


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

	matrix = matrix.copy()

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

	for index in range(len(matrix)):
		multiplier = lcm(*(c.denominator for c in matrix[index] if c))

		matrix[index] = tuple(c * multiplier for c in matrix[index])

	return matrix

def solve(matrix):
	def solve_internal(matrix, solution_initial = None, solutions = set()):
		if not len(matrix):
			return

		matrix = reduce(matrix)

		if any(not any(r[:-1]) and r[-1] for r in matrix):
			return

		solution = [None for _ in matrix[0][:-1]] if solution_initial is None else list(solution_initial)

		substitutions = [(i, r) for (i, r) in enumerate(matrix) if count(c for c in r[:-1] if c) == 1]
		substitutions.sort(key=itemgetter(0), reverse=True)

		for (index_row, row) in substitutions:
			index = min((i for (i, r) in enumerate(row) if r))

			if not (solution[index] is None or solution[index] == row[-1]):
				return

			if row[-1] < 0 or not row[-1].is_integer():
				return

			solution[index] = row[-1]

			del matrix[index_row]

		if not any(s is None for s in solution):
			solutions.add(tuple(solution))

			yield solution

			return

		if not len(matrix):
			return

		for (index, bound) in enumerate(get_bounds(matrix)):
			guess_solution = solution.copy()

			if guess_solution[index] is not None:
				continue

			guess_solution[index] = bound
			guess_solution = tuple(guess_solution)

			if guess_solution in solutions:
				continue

			guess_matrix = matrix.copy()

			for index_guess in range(len(guess_matrix)):
				guess_row = guess_matrix[index_guess]

				multiplier = guess_row[index_guess]

				if not multiplier:
					continue

				guess_matrix[index_guess] = (*(0 if i == index else c for (i, c) in enumerate(guess_row[:-1])), guess_row[-1] - multiplier * bound)

			yield from solve_internal(guess_matrix, guess_solution, solutions)

	return list(solve_internal(matrix))


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
