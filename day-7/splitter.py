#!/bin/env python3.14t


from re import compile
from sys import argv


ONES = compile(r'(S|\^)')
ZEROS = compile(r'\.')


def count_bits(number):
	result = 0

	while number:
		if number & 1:
			result += 1

		number >>= 1

	return result


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	input = list(read_file(filename))

	current = input[0]
	result = 0

	for row in input[1:]:
		split = row & current

		result += count_bits(split)

		split = split << 1 | split >> 1

		current = (current | split) & ~row

	print(result)


def read_file(filename):
	with open(filename) as file:
		for line in file:
			line = line.strip()
			line = ONES.sub('1', line)
			line = ZEROS.sub('0', line)

			yield int(line, base=2)


if __name__ == '__main__':
	main()
