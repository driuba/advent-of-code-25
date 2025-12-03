#!/bin/env python3.14t


from sys import argv


def main():
	if len(argv) == 1:
		process('input.txt')
	elif len(argv) == 2:
		process(argv[1])
	else:
		raise Exception('Multiple arguments are not supported.')


def process(filename):
	result = 0

	for batteries in read_file(filename):
		battery_result = 0

		for i in range(len(batteries) - 1):
			tens = 10 * batteries[i]

			if tens < battery_result % 10:
				continue

			battery_candidate = tens + max(batteries[i + 1:])

			if battery_candidate > battery_result:
				battery_result = battery_candidate

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
