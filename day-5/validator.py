#!/bin/env python3.14t


from operator import itemgetter
from re import compile
from sys import argv


PATTERN_RANGE = compile(r'(?P<start>\d+)-(?P<end>\d+)$')


def consolidate(ranges):
	ranges = sorted(ranges)

	count = 0
	result = ranges
	running = True

	while running:
		count += 1
		running = False

		print(count, len(result), end='\r', sep='\t')

		ranges = result
		result = []

		current = ranges[0]

		for (start, end) in ranges[1:]:
			(current_start, current_end) = current

			if current_end >= start - 1:
				running = True

				current = (current_start, max(current_end, end))
			else:
				result.append(current)

				current = (start, end)
		else:
			result.append(current)

	print()

	return result


def filter_valid(ranges, ids):
	if ids is None:
		ids = range(min(ranges, key=itemgetter(0))[0], max(ranges, key=itemgetter(1))[1] + 1)

	for id in ids:
		for (start, end) in ranges:
			if start <= id <= end:
				yield id


def main():
	count = len(argv) - 1

	assert count <= 2, 'More than one input is not supported'

	filename = argv[1] if count > 0 else 'input.txt'

	process(filename, count < 2)


def process(filename, valid_only):
	(ranges, ids) = read_file(filename, valid_only)

	if valid_only:
		ids_valid = set(filter_valid(ranges, ids))

		print(len(ids_valid))
	else:
		ranges = consolidate(ranges)

		print(sum([e - s + 1 for (s, e) in ranges]))


def read_file(filename, valid_only):
	with open(filename) as file:
		return (list(read_ranges(file)), set(read_ids(file)) if valid_only else None)


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
