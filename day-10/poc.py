#!/bin/env python3.14t


from fractions import Fraction
from itertools import product
from math import inf, lcm
from sys import argv


def analyze(_, buttons, joltages):
	try:
		matrix = [[Fraction(1) if i in b else Fraction(0) for i in range(len(joltages))] for b in buttons]
		matrix = transpose(matrix)
		matrix = [(*mr, Fraction(r)) for (mr, r) in zip(matrix, joltages)]

		index_row = -1

		while True:
			index_row += 1

			if index_row == len(matrix):
				break

			matrix[index_row:] = sorted(matrix[index_row:], key=lambda mr: min((i for (i, mc) in enumerate(mr) if mc), default=inf))

			row_current = matrix[index_row]
			index_column = min((i for (i, cc) in enumerate(row_current) if cc), default=-1)

			if index_column == -1:
				continue

			column_current = row_current[index_column]
			matrix[index_row] = row_current = tuple(c / column_current for c in row_current)

			for index in range(index_row + 1, len(matrix)):
				row = matrix[index]

				multiplier = row[index_column]

				if not multiplier:
					continue

				matrix[index] = tuple(c - multiplier * cc for (c, cc) in zip(row, row_current))

		matrix = [r for r in matrix if any(r)]

		#print(*matrix, sep='\n', end='\n\n')

		running = True
		substitutions_processed = set()

		while running:
			running = False

			substitutions = [r for r in matrix if r not in substitutions_processed and count(c for c in r[:-1] if c) == 1]

			for substitution in substitutions:
				substitutions_processed.add(substitution)

				running = True

				index_column = min(i for (i, s) in enumerate(substitution) if s)

				for index_row in range(len(matrix)):
					row = matrix[index_row]

					if substitution == row:
						continue

					multiplier = row[index_column]

					if not multiplier:
						continue

					matrix[index_row] = tuple(c - multiplier * sc for (c, sc) in zip(row, substitution))

		for index in range(len(matrix)):
			multiplier = lcm(*(c.denominator for c in matrix[index] if c))

			matrix[index] = (c * multiplier for c in matrix[index])
			matrix[index] = tuple(c.numerator if c.is_integer() else c for c in matrix[index])

		print(*matrix, sep='\n', end='\n\n')

		bounds = get_bounds(matrix)

		print(*bounds, end='\n\n')

		#equations = get_equations(matrix, joltages)

		#print(min((sum(vs) for vs in product(*(range(*b) for b in bounds)) if all((e(vs) for e in equations)))))
	finally:
		print()


def count(iterable):
	result = 0

	for _ in iterable:
		result += 1

	return result


def get_bounds(matrix):
	bounds = transpose([[c * r[-1] for c in r[:-1]] for r in matrix])
	bounds = [min((c for c in r if c > 0), default=0) for r in bounds]

	return bounds


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
