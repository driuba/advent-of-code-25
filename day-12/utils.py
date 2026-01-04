SYMETRIES = [
	(
		(0, 1, 2),
		(3, 4, 5),
		(6, 7, 8)
	),
	(
		(0, 3, 6),
		(1, 4, 7),
		(2, 5, 8)
	),
	(
		(2, 1, 0),
		(5, 4, 3),
		(8, 7, 6)
	),
	(
		(2, 5, 8),
		(1, 4, 7),
		(0, 3, 6)
	),
	(
		(6, 3, 0),
		(7, 4, 1),
		(8, 5, 2)
	),
	(
		(6, 7, 8),
		(3, 4, 5),
		(0, 1, 2)
	),
	(
		(8, 5, 2),
		(7, 4, 1),
		(6, 3, 0)
	),
	(
		(8, 7, 6),
		(5, 4, 3),
		(2, 1, 0)
	)
]


def empty(rows, columns):
	return [[0 for _ in range(columns)] for _ in range(rows)]


def format_cell(rgb, value):
	assert all((0 <= c <= 255 for c in rgb))

	code = ';'.join([
		'48',
		'2',
		*(str(c) for c in rgb)
	])

	return f'\033[{code}m \033[0m' if value else ' '


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
