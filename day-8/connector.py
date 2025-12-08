#!/bin/env python3.14t


from functools import reduce
from math import inf, sqrt
from sys import argv


def find_connections(boxes, count, distances):
	result = [(None, None, inf) for _ in range(count)]

	for i in range(len(boxes) - 1):
		for j in range(i + 1, len(boxes)):
			if distances[i][j] >= result[-1][-1]:
				continue

			for (index, (_, _, distance)) in enumerate(result):
				if distance > distances[i][j]:
					break
			else:
				continue

			result.insert(index, (boxes[i], boxes[j], distances[i][j]))

			result.pop()

	return result


def main():
	count = len(argv) - 1

	assert count <= 2, 'More than two arguments are not supported.'

	connections = int(argv[2]) if count >= 2 else 1000
	filename = argv[1] if count >= 1 else 'input.txt'

	process(connections, filename)


def process(count, filename):
	def construct_circut(box, connections):
		if box not in connections:
			return set()

		circut = connections.pop(box)

		for box_other in list(circut):
			circut |= connections.pop(box_other, set())

		for box_other in list(circut):
			circut |= construct_circut(box_other, connections)

		circut.add(box)

		return circut

	boxes = read_file(filename)

	distances = [[0. if i == j else inf for j in boxes] for i in boxes]

	for i in range(len(boxes) - 1):
		for j in range(i + 1, len(boxes)):
			distances[i][j] = distances[j][i] = sqrt(sum((c1 - c2) ** 2 for (c1, c2) in zip(boxes[i], boxes[j])))

	print('Calculated distances.')

	connections = {}

	for (a, b, _) in find_connections(boxes, count, distances):
		if a not in connections:
			connections[a] = set()

		if b not in connections:
			connections[b] = set()

		connections[a].add(b)
		connections[b].add(a)

	print('Built connections.')

	circuts = []

	for box in boxes:
		if box not in connections:
			continue

		circuts.append(construct_circut(box, connections))

	print(reduce(lambda a, l: a * l, sorted((len(c) for c in circuts), reverse=True)[:3]))


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
