#!/bin/env python3.14t


from itertools import product
from math import inf
from sys import argv


def analyze(_, buttons, joltages):
	try:
		matrix = [[1 if i in b else 0 for i in range(len(joltages))] for b in buttons]
		matrix = transpose(matrix)
		matrix = [(*mr, r) for (mr, r) in zip(matrix, joltages)]

		index_row = -1

		while True:
			matrix.sort(key=lambda mr: min((i for (i, mc) in enumerate(mr) if mc), default=inf))

			index_row += 1

			if index_row == len(matrix):
				break

			row_current = matrix[index_row]
			index_column = min((i for (i, cc) in enumerate(row_current) if cc), default=-1)

			if index_column == -1:
				continue

			column_current = row_current[index_column]
			matrix[index_row] = row_current = tuple(c // column_current for c in row_current)

			for index in range(index_row + 1, len(matrix)):
				row = matrix[index]

				multiplier = row[index_column] // column_current

				if not multiplier:
					continue

				matrix[index] = tuple(c - multiplier * cc for (c, cc) in zip(row, row_current))

		matrix = list({r for r in matrix if any(r)})

		print(*matrix, sep='\n', end='\n\n')

		# TODO: run substitutions if any, same idea as with previous while loop but this time work with lines that have only one variable and subtract that from every other row, repeat until no more substitutions are possible

		#bounds = get_bounds(matrix, joltages)

		#print(*bounds, end='\n\n')

		#equations = get_equations(matrix, joltages)

		#print(min((sum(vs) for vs in product(*(range(b, -1, -1) for b in bounds)) if all((e(vs) for e in equations)))))
	finally:
		print()


def get_bounds(matrix, results):
	bounds = [[mc * r for mc in mr] for (mr, r) in zip(transpose(matrix), results)]

	return [min((c for c in r if c)) for r in transpose(bounds)]


def get_equations(matrix, results):
	def get_check(variables, result):
		def check(coefficients):
			return sum((c * v for (c, v) in zip(coefficients, variables))) == result

		return check

	return [get_check(vs, r) for (vs, r) in zip(transpose(matrix), results)]


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
