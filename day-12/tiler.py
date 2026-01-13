#!/usr/bin/env python3.14t


from collections import deque
from fractions import Fraction
from functools import reduce
from random import shuffle
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


def calculate_greedy_metric(grid):
	return (
		Fraction(
			max(len(grid), len(grid[0])),
			min(len(grid), len(grid[0]))
		),
		sum((1 for r in grid for c in r if not c)),
		calculate_internal_area(grid)
	)


def calculate_internal_area(grid):
	areas = []
	visited = set()

	for (index_row, row) in enumerate(grid):
		for (index_column, cell) in enumerate(row):
			if cell:
				continue

			position = (index_row, index_column)

			if position in visited:
				continue

			area_current = set()

			queue = deque()
			queue.append(position)

			while queue:
				position = queue.popleft()

				if grid[position[0]][position[1]]:
					continue

				if position in visited:
					continue

				visited.add(position)

				area_current.add(position)

				if position[0] > 0:
					queue.append((position[0] - 1, position[1]))

				if position[0] < len(grid) - 1:
					queue.append((position[0] + 1, position[1]))

				if position[1] > 0:
					queue.append((position[0], position[1] - 1))

				if position[1] < len(grid[0]) - 1:
					queue.append((position[0], position[1] + 1))

			if all((0 < r < len(grid) - 1 and 0 < c < len(grid[0]) - 1 for (r, c) in area_current)):
				areas.append(area_current)

	return sum((len(a) for a in areas))


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
	assert rows >= 0
	assert columns >= 0

	def _iterate_cells(row):
		for index in range(-columns, len(row) + columns):
			if 0 <= index < len(row):
				yield row[index] or None
			else:
				yield None

	def _iterate_rows():
		for index in range(-rows, len(grid) + rows):
			if 0 <= index < len(grid):
				yield tuple(_iterate_cells(grid[index]))
			else:
				yield (None,) * (len(grid[0]) + columns * 2)

	return tuple(_iterate_rows())


def print_grid(grid):
	for row in grid:
		for cell in row:
			print(format_cell((191,) * 3, cell), end='')

		print()

	print()


def print_shapes(symetries):
	colors = generate_gradient(sum((len(ss) for (*_, ss) in symetries)), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255))

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


def print_solution(solution):
	if not solution:
		print('No greedy solution was found!')

		return

	cells = sorted(list(set((c for r in solution for c in r if c))))

	colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
	colors = generate_gradient(len(cells), *colors[:len(cells)])
	colors = {s:c for (c, s) in zip(colors, cells)}

	print(len(solution), 'x', len(solution[0]),sep='')

	for (index_row, row) in enumerate(solution):
		for (index_column, cell) in enumerate(row):
			text = '  '

			if cell:
				up = down = left = right = False

				if 0 < index_row and solution[index_row - 1][index_column] == cell:
					up = True

				if up:
					text = '╰╯'


			print(format_cell(cell and colors[cell], cell, text), end='')

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
		(vertices_tree, edges_tree, size, presents) = tree

		(vertices_present, edges_present) = reduce(
			lambda a, b: (a[0] + b[0], a[1] + b[1]),
			((v * p, e * p) for ((v, e, *_), p) in zip(shapes, presents))
		)

		print('x'.join((str(s) for s in size)), vertices_tree, edges_tree, '|', vertices_present, edges_present)
		print(*presents)

		if vertices_present <= vertices_tree and edges_present <= edges_tree:
			count += 1

			solution = solve(shapes, tree)

			print_solution(solution)
		else:
			print('No solution can fit!')

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
	(*_, (rows_max, columns_max), presents) = tree

	(rows_max, columns_max) = (min(rows_max, columns_max), max(rows_max, columns_max))

	shapes = [s[-1] for s in shapes]

	queue = deque()
	queue.append((None, presents, 0))

	states = set()

	while queue:
		(grid, presents, index) = queue.pop()

		index += 1

		if grid is None:
			rows_current = 0
			columns_current = 0
		else:
			rows_current = min(len(grid), len(grid[0]))
			columns_current = max(len(grid), len(grid[0]))

		if all((not p for p in presents)):
			return grid

		if grid is not None:
			state = (
				frozenset(
					generate_symetries(
						tuple((
							tuple((bool(c) for c in r))
							for r in grid
						))
					)
				),
				presents
			)

			if state in states:
				continue

			states.add(state)

		if grid is None:
			grid = ((None,) * 3,) * 3
		else:
			rows_extra = max(0, min(3, rows_max - rows_current))
			columns_extra = max(0, min(3, columns_max - columns_current))

			if rows_current == len(grid[0]) and columns_current == len(grid):
				(rows_extra, columns_extra) = (columns_extra, rows_extra)

			grid = pad(grid, rows_extra, columns_extra)

		metric_min = None
		placements_min = []

		for (index_shape, (symetries, count)) in enumerate(zip(shapes, presents)):
			if not count:
				continue

			for (index_symetry, shape) in enumerate(symetries):
				for (position, placement) in generate_placements(grid, shape):
					if metric_min is None:
						metric_min = calculate_greedy_metric(placement)
						placements_min = [(placement, index_shape, index_symetry)]

						continue

					metric = calculate_greedy_metric(placement)

					if metric < metric_min:
						metric_min = metric
						placements_min = [(placement, index_shape, index_symetry)]
					elif metric == metric_min:
						placements_min.append((placement, index_shape, index_symetry))

		for (placement, index_shape, index_symetry) in placements_min:
			placement = tuple((
				tuple((
					(index, index_shape, index_symetry) if c is True else c
					for c in r
				))
				for r in placement
			))

			queue.append((
				placement,
				tuple((p - 1 if i == index_shape else p for (i, p) in enumerate(presents))),
				index
			))

	return None


if __name__ == '__main__':
	main()
