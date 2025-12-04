#!/bin/env python3.14t


from sys import argv


VALUE_MAX = 9


def calculate(batteries, scale, count = 0):
	if scale < 0:
		return (0, count)

	(index, value, count) = get_max(batteries[:len(batteries) - scale], count)

	(value_next, count) = calculate(batteries[index + 1:], scale - 1, count)

	return (value * 10 ** scale + value_next, count)


def get_max(batteries, count):
	index = -1
	value = -1

	for [index_candidate, value_candidate] in enumerate(batteries):
		count += 1

		if value_candidate > value:
			index = index_candidate
			value = value_candidate

		if value >= VALUE_MAX:
			break

	if index < 0 or value < 0:
		raise Exception('Failed to resolve maximume value.')

	return (index, value, count)


def main():
	length = len(argv)

	if length > 3:
		raise Exception('More than two arguments are not supported.')

	filename = argv[1] if len(argv) > 1 else 'input.txt'
	scale = int(argv[2]) - 1 if len(argv) > 2 else 11

	process(filename, scale)


def process(filename, scale):
	result = 0

	for batteries in read_file(filename):
		(battery_result, iteration_count) = calculate(batteries, scale)

		print(battery_result, iteration_count, iteration_count / len(batteries))

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
