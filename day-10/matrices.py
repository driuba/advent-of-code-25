def add_member(matrix_a, matrix_b):
	"""
	Expected input: nested list
	"""

	return _apply_memberwise(matrix_a, matrix_b, lambda a, b: a + b)


def copy(matrix):
	return [list(r) for r in matrix]


def identity(size, element_type = int):
	return [
		[
			element_type(1) if c == r else element_type(0)
			for c in range(size)
		]
		for r in range(size)
	]


def multiply(matrix_a, matrix_b):
	"""
	Expected input: nested list
	"""

	assert matrix_a
	assert matrix_b
	assert all(ra and len(ra) == len(matrix_a[0]) for ra in matrix_a)
	assert all(rb and len(rb) == len(matrix_b[0]) for rb in matrix_b)
	assert len(matrix_a[0]) == len(matrix_b)

	matrix_b = transpose(matrix_b)

	return [
		[
			sum((
				ca * cb
				for (ca, cb)
				in zip(ra, rb)
			))
			for rb in matrix_b
		]
		for ra in matrix_a
	]


def multiply_member(matrix_a, matrix_b):
	"""
	Expected input: nested list
	"""

	return _apply_memberwise(matrix_a, matrix_b, lambda a, b: a * b)


def multiply_scalar(scalar, matrix):
	"""
	Expected input: nested list
	"""

	assert matrix
	assert all(r and len(r) == len(matrix[0]) for r in matrix)

	return [[scalar * c for c in r] for r in matrix]


def transpose(matrix):
	"""
	Expected input: nested list
	"""

	assert matrix
	assert all(r and len(r) == len(matrix[0]) for r in matrix)

	return [list(r) for r in _transpose(matrix)]


def _apply_memberwise(matrix_a, matrix_b, operation):
	assert matrix_a
	assert matrix_b
	assert all(ra and len(ra) == len(matrix_a[0]) for ra in matrix_a)
	assert all(rb and len(rb) == len(matrix_b[0]) for rb in matrix_b)
	assert len(matrix_a) == len(matrix_b)
	assert len(matrix_a[0]) == len(matrix_b[0])

	return [
		[
			operation(ca, cb)
			for (ca, cb)
			in zip(ra, rb)
		]
		for (ra, rb)
		in zip(matrix_a, matrix_b)
	]


def _transpose(matrix):
	def transpose_column(column):
		for row in range(len(matrix)):
			yield matrix[row][column]

	def transpose_rows():
		for column in range(len(matrix[0])):
			yield transpose_column(column)

	return transpose_rows()

