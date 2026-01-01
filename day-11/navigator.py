#!/bin/env python3.14t


from collections import deque
from sys import argv


YOU = 'you'
OUT = 'out'


def find_paths(network):
	def iterate():
		try:
			queue = deque()

			queue.append([YOU])

			while queue:
				path = queue.pop()
				machine = path[-1]

				if machine == OUT:
					print(*path)

					yield path

					continue

				for connection in network[machine] - set(path):
					queue.append([*path, connection])
		finally:
			print()

	return list(iterate())


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	print(
		'The result is',
		len(
			find_paths(
				read_file(filename)
			)
		)
	)


def read_file(filename):
	def iterate():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				[machine, connections] = line.split(':')

				yield (
					machine.strip(),
					frozenset(connections.strip().split())
				)

	return {m:cs for (m, cs) in iterate()}


if __name__ == '__main__':
	main()
