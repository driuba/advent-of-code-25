#!/bin/env python3.14t

from math import inf
from sys import argv


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	def iterate(areas):
		for row in range(len(areas)):
			for column in range(row, len(areas[row])):
				yield areas[row][column]

	tiles = read_file(filename)

	areas = [[1 if i == j else -inf for j in tiles] for i in tiles]

	for row in range(len(tiles) - 1):
		for column in range(row + 1, len(tiles)):
			areas[row][column] = areas[column][row] = (abs(tiles[row][0] - tiles[column][0]) + 1) * (abs(tiles[row][1] - tiles[column][1]) + 1)

	print(max(iterate(areas)))


def read_file(filename):
	def read():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				if line:
					yield tuple(int(c) for c in line.split(','))

	return list(read())


if __name__ == '__main__':
	main()
