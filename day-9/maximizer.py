#!/bin/env python3.14t


from math import inf
from sys import argv


def cross(a, b):
	return a[0] * b[1] - a[1] * b[0]


def find_max_area(tiles):
	def iterate_invalid():
		for (i, (_, n)) in enumerate(tiles):
			if n < 0:
				((x1, y1), _) = tiles[(i - 1) % len(tiles)]
				((x2, y2), _) = tiles[(i + 1) % len(tiles)]

				yield ((min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)))

	ranges_invalid = list(iterate_invalid())

	result = -inf

	for (index, ((x1_initial, y1_initial), _)) in enumerate(tiles):
		for ((x2_initial, y2_initial), _) in tiles[index:]:
			x1 = min(x1_initial, x2_initial)
			y1 = min(y1_initial, y2_initial)
			x2 = max(x1_initial, x2_initial)
			y2 = max(y1_initial, y2_initial)

			if any((x1 < x2_i and y1 < y2_i and x2 > x1_i and y2 > y1_i for ((x1_i, y1_i), (x2_i, y2_i)) in ranges_invalid)):
				continue

			area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

			if result < area:
				result = area

	return result


def find_winding(points):
	x_min = inf
	x_max = -inf
	y_min = inf
	y_max = -inf

	for ((x, y), _) in points:
		if x_min > x:
			x_min = x

		if x_max < x:
			x_max = x

		if y_min > y:
			y_min = y

		if y_max < y:
			y_max = y

	for ((x, y), normal) in points:
		if not (x == x_min or x == x_max or y == y_min or y == y_max):
			continue

		if normal:
			return normal // abs(normal)

	return 0


def get_normals(points):
	vectors = get_vectors(points)

	def iterate():
		for (a, b) in zip(vectors[:-1], vectors[1:]):
			yield cross(a, b)

		yield cross(vectors[-1], vectors[0])

	return list(iterate())


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
	tiles = read_file(filename)
	tiles = list(zip(tiles, get_normals(tiles)))

	winding = find_winding(tiles)

	tiles = [(p, n * winding) for (p, n) in tiles]

	print(find_max_area(tiles))


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
