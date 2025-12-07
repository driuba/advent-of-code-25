#!/bin/env python3.14t


from functools import reduce
from sys import argv


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one arguments are not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	def add(*inputs):
		return reduce(lambda a, i: a + i, inputs)

	def multiply(*inputs):
		return reduce(lambda a, i: a * i, inputs)

	input = list(zip(*read_file(filename)))

	result = 0

	for task in input:
		match task[-1]:
			case '+':
				result += add(*task[:-1])
			case '*':
				result += multiply(*task[:-1])
			case _:
				raise Exception(f'Unuspported operation: {", ".join(task)}.')

	print(result)


def read_file(filename):
	with open(filename) as file:
		for line in file:
			line = line.strip()

			yield [int(p) if p.isdigit() else p for p in line.split()]


if __name__ == '__main__':
	main()
