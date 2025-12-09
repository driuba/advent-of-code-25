#!/bin/env python3.14t

from math import inf
from sys import argv


def cross(a, b):
	return a[0] * b[1] - a[1] * b[0]


def find_winding(points, normals):
	x_min = inf
	x_max = -inf
	y_min = inf
	y_max = -inf

	for (x, y) in points:
		if x_min > x:
			x_min = x

		if x_max < x:
			x_max = x

		if y_min > y:
			y_min = y

		if y_max < y:
			y_max = y

	for (index, (x, y)) in enumerate(points):
		if not (x == x_min or x == x_max or y == y_min or y == y_max):
			continue

		normal = normals[index]

		if normal:
			return normal // abs(normal)

	return 0


def get_vectors(points):
	def iterate():
		(x1, y1) = points[-1]
		(x2, y2) = points[0]

		yield (x2 - x1, y2 - y1)

		for ((x1, y1), (x2, y2)) in zip(points[:-1], points[1:]):
			yield (x2 - x1, y2 - y1)

	return list(iterate())


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
	steps = get_vectors(tiles)

	print(*tiles)
	print(*steps)

	directions = []

	for (a, b) in zip(steps[:-1], steps[1:]):
		directions.append(cross(a, b))
	else:
		directions.append(cross(b, steps[0]))

	print(directions)

	print(find_winding(tiles, directions))

	return

	areas = [[1 if i == j else -inf for j in tiles] for i in tiles]

	for row in range(len(tiles) - 1):
		for column in range(row + 1, len(tiles)):
			(x1, y1) = tiles[row]
			(x2, y2) = tiles[column]

			areas[row][column] = areas[column][row] = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

	print(max(iterate(areas)))


def read_file(filename):
	def read():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				if line:
					[x, y] = line.split(',')

					yield (int(x), int(y))

	return list(read())


if __name__ == '__main__':
	main()
