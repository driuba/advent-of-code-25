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

	input = read_file(filename)

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
	def reconstruct(numbers):
		column = []

		for number in numbers:
			if number:
				column.append(int(number))
			else:
				yield column

				column = []
		else:
			yield column

	result = []

	with open(filename) as file:
		for line in file:
			line = line.strip('\r\n')

			result.append(line[::-1])

	numbers = result[:-1]
	operations = result[-1].split()

	numbers = [''.join(c).strip() for c in zip(*numbers)]
	result = [(*ns, o) for (ns, o) in zip(reconstruct(numbers), operations)]

	return result


if __name__ == '__main__':
	main()
