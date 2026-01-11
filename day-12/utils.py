def format_cell(rgb, value):
	assert all((0 <= c <= 255 for c in rgb))

	code_true = ';'.join([
		'48',
		'2',
		*(str(c) for c in rgb)
	])

	code_false = ';'.join(['48', '2', '0', '0', '0'])

	return f'\033[{code_true if value else code_false}m  \033[0m'


def generate_gradient(steps, *stops):
	assert len(stops) > 1
	assert all((all((0 <= c <= 255 for c in cs)) for cs in stops))
	assert steps >= len(stops)

	def _generate_stage(start, stop, steps):
		(start_r, start_g, start_b) = start
		(stop_r, stop_g, stop_b) = stop

		step_r = (stop_r - start_r) / (steps + 1)
		step_g = (stop_g - start_g) / (steps + 1)
		step_b = (stop_b - start_b) / (steps + 1)

		for step in range(1, steps + 1):
			yield (round(start_r + step_r * step), round(start_g + step_g * step), round(start_b + step_b * step))

		yield stop

	def _generate():
		step = (steps - len(stops)) / (len(stops) - 1)

		stages = [round(step)] * (len(stops) - 2)

		stages.append(steps - len(stops) - sum(stages))

		yield stops[0]

		for (start, stop, stage) in zip(stops[:-1], stops[1:], stages):
			yield from _generate_stage(start, stop, stage)

	return list(_generate())


def generate_symetries(grid):
	def _generate():
		yield grid

		a = reverse(grid)
		b = transpose(grid)

		yield a
		yield b

		a = transpose(a)
		b = reverse(b)

		yield a
		yield b

		a = reverse(a)

		yield a
		yield transpose(b)
		yield transpose(a)

	return list(set(_generate()))


def reverse(grid):
	return tuple(_reverse(grid))


def transpose(grid):
	assert grid
	assert all(len(r) == len(grid[0]) for r in grid)

	return tuple((tuple(r) for r in _transpose(grid)))


def trim(grid):
	assert grid
	assert all(len(r) == len(grid[0]) for r in grid)

	grid = tuple((r for r in grid if any(r)))
	grid = transpose(grid)
	grid = tuple((r for r in grid if any(r)))
	grid = transpose(grid)

	return grid


def _reverse(grid):
	return reversed(grid)


def _transpose(grid):
	def _transpose_column(column):
		for row in range(len(grid)):
			yield grid[row][column]

	def _transpose_rows():
		for column in range(len(grid[0])):
			yield _transpose_column(column)

	return _transpose_rows()

