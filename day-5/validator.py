#!/bin/env python3.14t


from re import compile
from sys import argv


PATTERN_RANGE = compile(r'(?P<start>\d+)-(?P<end>\d+)$')


def filter_valid(ranges, ids):
	for id in ids:
		for (start, end) in ranges:
			if start <= id <= end:
				yield id


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one input is not supported'

	filename = argv[1] if count > 0 else 'input.txt'

	process(filename)


def process(filename):
	(ranges, ids) = read_file(filename)

	ids_valid = set(filter_valid(ranges, ids))

	print(len(ids_valid))


def read_file(filename):
	with open(filename) as file:
		return (list(read_ranges(file)), set(read_ids(file)))


def read_ids(file):
	for line in file:
		line = line.strip()

		if not line:
			continue

		yield int(line)


def read_ranges(file):
	for line in file:
		line = line.strip()

		if not line:
			break

		match = PATTERN_RANGE.match(line)

		if not match:
			continue

		yield (int(match.group('start')), int(match.group('end')))


if __name__ == '__main__':
	main()
