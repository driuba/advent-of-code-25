#!/bin/env python3.14t


from re import compile
from sys import argv


ONES = compile(r'(S)')
TWOS = compile(r'\^')
ZEROS = compile(r'\.')


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	manifold = list(read_file(filename))

	beam = manifold[0]

	for splitters in manifold[1:]:
		current = [0 for _ in beam]
		for (index, (particle, splitter)) in enumerate(zip(beam, splitters)):
			if splitter and particle:
				current[index - 1] += particle
				current[index + 1] += particle
			elif particle:
				current[index] += particle

		beam = current

	print(sum(beam))


def read_file(filename):
	with open(filename) as file:
		for line in file:
			line = line.strip()
			line = ONES.sub('1', line)
			line = TWOS.sub('2', line)
			line = ZEROS.sub('0', line)

			yield [int(c) for c in line]


if __name__ == '__main__':
	main()
