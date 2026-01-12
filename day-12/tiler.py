#!/bin/env python3.14t


from collections import deque
from functools import reduce
from re import compile
from sys import argv

from utils import (
	format_cell,
	generate_gradient,
	generate_symetries,
	trim
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


def generate_placements(grid, shape):
	def _iterate_cells(row, shape_row, index_column):
		for (index, cell) in enumerate(row):
			if index_column <= index < index_column + len(shape_row):
				yield cell or shape_row[index - index_column]
			else:
				yield cell

	def _iterate_rows(index_row, index_column):
		for (index, row) in enumerate(grid):
			if index_row <= index < index_row + len(shape):
				yield tuple(_iterate_cells(row, shape[index - index_row], index_column))
			else:
				yield row

	for (index_row, index_column) in generate_positions(grid, shape):
		placement = tuple(_iterate_rows(index_row, index_column))

		yield ((index_row, index_column), trim(placement))


def generate_positions(grid, shape):
	for index_row in range(0, len(grid) - len(shape) + 1):
		for index_column in range(0, len(grid[0]) - len(shape[0]) + 1):
			if all((all((not (c and grid[index_row + ir][index_column + ic]) for (ic, c) in enumerate(r))) for (ir, r) in enumerate(shape))):
				yield (index_row, index_column)


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def pad(grid, rows, columns):
	def _iterate_cells(row):
		for index in range(-columns, len(row) + columns):
			if 0 <= index < len(row):
				yield row[index]
			else:
				yield False

	def _iterate_rows():
		for index in range(-rows, len(grid) + rows):
			if 0 <= index < len(grid):
				yield tuple(_iterate_cells(grid[index]))
			else:
				yield (False,) * (len(grid[0]) + columns * 2)

	return tuple(_iterate_rows())


def print_grid(grid):
	for row in grid:
		for cell in row:
			print(format_cell((191,) * 3, cell), end='')

		print()

	print()


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

	trees = [(
		r * c,
		r * (c - 1) + (r - 1) * c,
		(r, c),
		p
	) for ((r, c), p) in trees]

	print_shapes(shapes)

	count = 0

	for tree in trees:
		(vertices, edges, size, presents) = tree

		print('x'.join((str(s) for s in size)), vertices, edges)
		print(*presents)

		if solve(shapes, tree):
			count += 1

		print()

	print()

	print(count)


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
			tuple(int(p) for p in presents.split())
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


def solve(shapes, tree):
	def placement_area(symetries):
		(placement, *_) = symetries

		return len(placement) * len(placement[0])

	(vertices_max, edges_max, (rows_max, columns_max), presents) = tree

	(rows_max, columns_max) = (min(rows_max, columns_max), max(rows_max, columns_max))

	(vertices, edges) = reduce(
		lambda a, b: (a[0] + b[0], a[1] + b[1]),
		((v * p, e * p) for ((v, e, *_), p) in zip(shapes, presents))
	)

	shapes = [s[-1] for s in shapes]

	if vertices > vertices_max or edges > edges_max:
		return False

	return True

	queue = deque()

	queue.append((frozenset([None]), presents))

	states_checked = set()

	while queue:
		state = queue.pop()

		if state in states_checked:
			continue
		else:
			states_checked.add(state)

		((grid, *_), presents) = state

		if grid is None:
			rows_current = 0
			columns_current = 0
		else:
			rows_current = min(len(grid), len(grid[0]))
			columns_current = max(len(grid), len(grid[0]))

		if rows_current > rows_max or columns_current > columns_max:
			continue

		if all((not p for p in presents)):
			print(len(grid), len(grid[0]))
			print_grid(grid)

			return True

		rows_extra = max(0, min(3, rows_max - rows_current))
		columns_extra = max(0, min(3, columns_max - columns_current))

		if grid is None:
			grid = ((False,) * 3,) * 3
		else:
			grid = pad(grid, rows_extra, columns_extra)

		for (index_shape, (symetries, count)) in enumerate(zip(shapes, presents)):
			if not count:
				continue

			placements = {}

			for (index_symetry, shape) in enumerate(symetries):
				for (position, placement) in generate_placements(grid, shape):
					placement = frozenset(generate_symetries(placement))

					if placement not in placements:
						placements[placement] = (*position, index_shape, index_symetry)

			if not placements:
				continue

			presents_remaining = tuple((p - 1 if i == index_shape else p for (i, p) in enumerate(presents)))

			placement = min(placements, key=placement_area)

			queue.append((placement, presents_remaining))

	return False


if __name__ == '__main__':
	main()
