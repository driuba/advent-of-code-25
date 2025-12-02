#!/bin/env python3.14t

from re import compile


pattern = compile(r'^(?P<section>\d+)(?P=section)$')


def main():
	result = 0

	for (start, end) in read_input():
		for id in range(start, end + 1):
			if (pattern.match(str(id))):
				result += id

	print(result)


def read_input(filename = 'input.txt'):
	with open(filename) as file:
		content = file.read().strip()

		for interval in content.split(','):
			[start, end] = interval.split('-')

			yield (int(start), int(end))


if __name__ == '__main__':
	main()
