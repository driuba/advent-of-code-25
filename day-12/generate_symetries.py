#!/bin/env python3.14t


from itertools import product
from re import compile


REDUCTION = compile(r'(R{2}|T{2}|(RT){4})')


def _reverse(grid):
	return tuple(reversed(grid))


def _transpose(grid):
	assert grid
	assert all(len(r) == len(grid[0]) for r in grid)

	def _transpose_column(column):
		for row in range(len(grid)):
			yield grid[row][column]

	def _transpose_rows():
		for column in range(len(grid[0])):
			yield _transpose_column(column)

	return tuple((tuple(r) for r in _transpose_rows()))


def generate_grid(rows, columns):
	def _generate():
		offset = 0

		for _ in range(rows):
			yield tuple((offset + c for c in range(columns)))

			offset += columns

	return tuple(_generate())


def main():
	grids = [
		generate_grid(3, 3),
		generate_grid(4, 4),
		generate_grid(5, 5),
		generate_grid(3, 10),
		generate_grid(3, 11),
		generate_grid(11, 5),
		generate_grid(12, 5),
		generate_grid(10, 8),
		generate_grid(10, 6),
	]

	for grid in grids:
		print_grid(rotate_0(grid))
		print_grid(rotate_90(grid))
		print_grid(rotate_180(grid))
		print_grid(rotate_270(grid))
		print_grid(reflect_diagonal_anti(grid))
		print_grid(reflect_diagonal_main(grid))
		print_grid(reflect_horizontal(grid))
		print_grid(reflect_vertical(grid))

	print_transformations()

	transformations = [
		('', rotate_0),
		('RT', rotate_90),
		('RTRT', rotate_180),
		('RTRTRT', rotate_270),
		('TRTRT', reflect_diagonal_anti),
		('T', reflect_diagonal_main),
		('TRT', reflect_horizontal),
		('R', reflect_vertical),
	]

	for grid in grids:
		transformations_grid = {}

		for ((tag_a, transform_a), (tag_b, transform_b)) in product(transformations, repeat=2):
			grid_transformed = transform_b(transform_a(grid))

			if grid_transformed not in transformations_grid:
				transformations_grid[grid_transformed] = []

			transformations_grid[grid_transformed].append(tag_a + tag_b)

		for grid_transformed in transformations_grid:
			transformations_grid[grid_transformed] = reduce_transformations(transformations_grid[grid_transformed])

		print(len(transformations_grid), *sorted((t for [t, *_] in transformations_grid.values())), sep=',')


def print_grid(grid):
	for row in grid:
		for cell in row:
			print(f'{cell: ^5}', end='')

		print()
	
	print()


def print_transformations():
	transformations = [
		'',
		'R',
		'T',
		'TRT',
		'TRTRT',
		'RT',
		'RTRT',
		'RTRTRT'
	]

	transformations = [a + b for (a, b) in product(transformations, repeat=2)]
	transformations = reduce_transformations(transformations)

	print(len(transformations), *transformations, sep='\n')


def reduce_transformations(transformations):
	transformations = list(transformations)

	for index in range(len(transformations)):
		completed = False
		transformation = transformations[index]

		while not completed:
			transformation_reduced = REDUCTION.sub('', transformation)

			completed = transformation == transformation_reduced

			transformation = transformation_reduced

		transformations[index] = transformation

	transformations = set(transformations)
	transformations = sorted(transformations, key=lambda t: (len(t), t))

	return transformations


def reflect_diagonal_anti(grid):
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)

	return grid


def reflect_diagonal_main(grid):
	grid = _transpose(grid)

	return grid


def reflect_horizontal(grid):
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)

	return grid


def reflect_vertical(grid):
	grid = _reverse(grid)

	return grid


def rotate_0(grid):
	return grid


def rotate_90(grid):
	grid = _reverse(grid)
	grid = _transpose(grid)

	return grid


def rotate_180(grid):
	grid = _reverse(grid)
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)

	return grid


def rotate_270(grid):
	grid = _reverse(grid)
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)
	grid = _reverse(grid)
	grid = _transpose(grid)

	return grid


if __name__ == '__main__':
	main()
