#!/bin/env python3.14t


from re import compile
from sys import argv

from utils import (
	SYMETRIES
)


SHAPE_INDEX = compile(r'^\d+:$')
TREE_SIZE = compile(r'^\d+x\d+:')


def generate_symetries(shapes):
	def _generate(shape):
		for symetry in SYMETRIES:
			yield tuple((
				tuple((
					shape[c // 3][c % 3]
					for c in r
				))
				for r in symetry
			))

	return [list(set(_generate(s))) for s in shapes]


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	(shapes, trees) = read_file(filename)

	shapes = generate_symetries(shapes)

	for symetries in shapes:
		for shape in symetries:
			for row in shape:
				print(' ', *(f'{('█' if c else ' ')}' for c in row), sep='')

			print()

		print()

	print()

	# TODO: maybe calculate areas and perimeters for some sort of ranking
	# TODO: implement my brute force depth first search
	#   start the search with a single corner
	#   consider only adjacent positions to the current figure
	#   it should be possible to prune the search by tracking overall shape and remaining shapes

	# for (size, presents) in trees:
	# 	print(size, *presents)


def read_file(filename):
	def _get_shape(file):
		def _iterate():
			for line in file:
				line = line.strip()

				if not line:
					return

				yield tuple((1 if c == '#' else 0 for c in line))

		return tuple(_iterate())

	def _get_tree(line):
		[size, presents] = line.split(':')

		[width, length] = size.strip().split('x')

		return (
			(int(length), int(width)),
			[int(p) for p in presents.split()]
		)

	shapes = []
	trees = []

	with open(filename) as file:
		while True:
			line = file.readline()

			if not line:
				break

			line = line.strip()

			if SHAPE_INDEX.match(line):
				shapes.append(_get_shape(file))
			elif TREE_SIZE.match(line):
				trees.append(_get_tree(line))

	return (shapes, trees)

if __name__ == '__main__':
	main()
