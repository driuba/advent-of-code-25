#!/bin/env python3.14t


from sys import argv
from operator import itemgetter


def calculate(batteries, scale):
	if scale < 0:
		return 0

	[index, value] = max(enumerate(batteries[:len(batteries) - scale]), key=itemgetter(1))

	return value * 10 ** scale + calculate(batteries[index + 1:], scale - 1)


def main():
	length = len(argv)

	if length > 3:
		raise Exception('Multiple arguments are not supported.')

	filename = argv[1] if len(argv) > 1 else 'input.txt'
	scale = int(argv[2]) - 1 if len(argv) > 2 else 11

	process(filename, scale)


def process(filename, scale):
	result = 0

	for batteries in read_file(filename):
		battery_result = calculate(batteries, scale)

		print(battery_result)

		result += battery_result

	print(result)


def read_file(filename):
	with open(filename) as file:
		for line in file:
			line = line.strip()

			if line:
				print(line, end=' ')

				yield [int(c) for c in line]


if __name__ == '__main__':
	main()
