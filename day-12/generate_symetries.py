#!/bin/env python3.14t


from itertools import product


def main():
	"""This function generates all of the distinct symetries of a 3x3 square grid."""
	symetries = [
		(0, 1, 2, 3, 4, 5, 6, 7, 8), # rotation 0
		(6, 3, 0, 7, 4, 1, 8, 5, 2), # rotation 90
		(8, 7, 6, 5, 4, 3, 2, 1, 0), # rotation 180
		(2, 5, 8, 1, 4, 7, 0, 3, 6), # rotation 270
		(6, 7, 8, 3, 4, 5, 0, 1, 2), # reflection vertical
		(2, 1, 0, 5, 4, 3, 8, 7, 6), # reflection horizontal
		(0, 3, 6, 1, 4, 7, 2, 5, 8), # reflection main diagonal
		(8, 5, 2, 7, 4, 1, 6, 3, 0), # reflection anti diagonal
	]

	result = set(symetries)

	for (a, b) in product(symetries, repeat=2):
		result.add(tuple((a[i] for i in b)))

	result = [
		tuple((
			tuple((
				r[i * 3 + j]
				for j in range(3)
			))
			for i in range(3)
		))
		for r in result
	]

	result.sort()

	print(repr(result))


if __name__ == '__main__':
	main()
