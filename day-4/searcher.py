#!/bin/env python3.14t


from sys import argv


KERNEL = [
	[1, 1, 1],
	[1, 0, 1],
	[1, 1, 1]
]


def apply_kernel(window):
	assert len(window) == len(KERNEL), 'Window size must match kernel size.'
	assert len(window[0]) == len(KERNEL[0]), 'Window size must match kernel size.'

	width = len(window[0])

	for row in window:
		assert len(row) == width, 'Window width must be consistent.'

	sum = 0

	for row in range(len(KERNEL)):
		for column in range(len(KERNEL[0])):
			sum += window[row][column] * KERNEL[row][column]

	return sum


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one input is not supported.'

	filename = argv[1] if count else 'input.txt'

	process(filename)


def process(filename):
	matrix = read_file(filename)

	for row in matrix:
		row.insert(0, 0)
		row.insert(len(row), 0)

	matrix.insert(0, [0 for _ in matrix[0]])
	matrix.insert(len(matrix), [0 for _ in matrix[0]])

	width = len(matrix[0])

	for row in matrix:
		assert len(row) == width, 'Input width must be consistent.'

	result = [[0 for _ in r] for r in matrix]

	for row in range(1, len(matrix) - 1):
		for column in range(1, len(matrix[0]) - 1):
			result[row][column] = 1 if apply_kernel([r[column - 1:column + 2] for r in matrix[row - 1:row + 2]]) < 4 else 0
			result[row][column] *= matrix[row][column]

	print(sum([sum(r) for r in result]))


def read_file(filename):
	matrix = []

	with open(filename) as file:
		for line in file:
			line = line.strip()

			if not line:
				continue

			matrix.append([1 if c == '@' else 0 for c in line])

	return matrix


if __name__ == '__main__':
	main()
