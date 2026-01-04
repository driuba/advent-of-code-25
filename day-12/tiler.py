#!/bin/env python3.14t


from re import compile
from sys import argv

from utils import (
	format_cell,
	generate_gradient,
	generate_symetries
)


SHAPE_INDEX = compile(r'^\d+:$')
TREE_SIZE = compile(r'^\d+x\d+:')


def count_edges(shape):
	def _iterate_kernel(target_row, target_column):
		for index_row in range(target_row - 1, target_row + 2):
			if not 0 <= index_row <= 2:
				continue

			for index_column in range(target_column - 1, target_column + 2):
				if not 0 <= index_column <= 2:
					continue

				if index_row == target_row and index_column == target_column:
					continue

				if index_row != target_row and index_column != target_column:
					continue

				if shape[index_row][index_column]:
					yield 1

	def _iterate():
		for (index_row, row) in enumerate(shape):
			for (index_column, cell) in enumerate(row):
				if cell:
					yield from _iterate_kernel(index_row, index_column)

	return sum(_iterate()) // 2


def count_vertices(shape):
	def _iterate():
		for row in shape:
			for cell in row:
				if cell:
					yield 1

	return sum(_iterate())


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def print_shapes(symetries):
	colors = generate_gradient(sum((len(ss) for (*_, ss) in symetries)), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255))

	print(*(format_cell(c, True) for c in colors), sep='', end='\n\n')

	for (index_symetry, (vertices, edges, shapes)) in enumerate(symetries):
		color_offset = sum((len(ss) for (*_, ss) in symetries[:index_symetry]))
		shapes = list(shapes)

		print(vertices, edges)

		for row in range(3):
			for (index_shape, shape) in enumerate(shapes):
				print(*(format_cell(colors[color_offset + index_shape], c) for c in shape[row]), sep='', end='\t')

			print()

		print()

	print()


def process(filename):
	(shapes, trees) = read_file(filename)

	shapes = [(count_vertices(s), count_edges(s), generate_symetries(s)) for s in shapes]

	print_shapes(shapes)

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

				yield tuple((c == '#' for c in line))

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
