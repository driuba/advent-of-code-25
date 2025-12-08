#!/bin/env python3.14t


from math import inf, sqrt
from operator import itemgetter
from sys import argv


def find_connections(boxes, distances):
	def iterate():
		for i in range(len(boxes) - 1):
			for j in range(i + 1, len(boxes)):
				yield (boxes[i], boxes[j], distances[i][j])

	return sorted(iterate(), key=itemgetter(2))


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	boxes = read_file(filename)

	distances = [[0. if i == j else inf for j in boxes] for i in boxes]

	for i in range(len(boxes) - 1):
		for j in range(i + 1, len(boxes)):
			distances[i][j] = distances[j][i] = sqrt(sum((c1 - c2) ** 2 for (c1, c2) in zip(boxes[i], boxes[j])))

	print('Calculated distances.')

	circuts = []

	for (a, b, _) in find_connections(boxes, distances):
		current = {a, b}

		for circut in circuts.copy():
			if a in circut or b in circut:
				current |= circut

				circuts.remove(circut)

		circuts.append(current)

		if len(circuts[0]) == len(boxes):
			break

	print('Built circut.')

	print(a[0] * b[0])


def read_file(filename):
	def read(filename):
		with open(filename) as file:
			for line in file:
				line = line.strip()

				if line:
					yield tuple(int(p) for p in line.split(','))

	return list(read(filename))


if __name__ == '__main__':
	main()
