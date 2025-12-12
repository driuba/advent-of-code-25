#!/bin/env python3.14t


from collections import deque
from math import inf, sqrt
from sys import argv

from models import Heap


def find_joltage_path(machine):
	def distance(joltage_candidate, joltage_target):
		return sum(abs(jc - jt) for (jc, jt) in zip(joltage_candidate, joltage_target))

	def iterate_buttons(joltage, joltage_target, buttons):
		for button in buttons:
			joltage_candidate = tuple(j + 1 if i in button else j for (i, j) in enumerate(joltage))

			if any(jc > jt for (jc, jt) in zip(joltage_candidate, joltage_target)):
				continue

			yield (joltage_candidate, button)

	def iterate_path(joltage, joltage_paths):
		while joltage:
			yield joltage

			joltage = joltage_paths[joltage]

	try:
		(_, buttons, joltage_target) = machine

		step_max = max((len(b) for b in buttons))

		queue = Heap()

		joltage_initial = tuple(0 for _ in joltage_target)

		joltage_paths = {joltage_initial: None}

		queue.push(
			distance(joltage_initial, joltage_target),
			joltage_initial
		)

		while queue:
			(_, joltage) = queue.pop()

			print(joltage_target, joltage, end='\r')

			if joltage == joltage_target:
				result = list(iterate_path(joltage, joltage_paths))

				result.reverse()

				return result[1:]

			for (joltage_candidate, button) in iterate_buttons(joltage, joltage_target, buttons):
				steps = sum((1 for _ in iterate_path(joltage, joltage_paths))) + 1

				if joltage_candidate not in joltage_paths:
					joltage_paths[joltage_candidate] = joltage

					queue.push(
						steps + distance(joltage_candidate, joltage_target) / step_max,
						joltage_candidate
					)
				elif steps < sum((1 for _ in iterate_path(joltage_candidate, joltage_paths))):
					joltage_paths[joltage_candidate] = joltage
	finally:
		print()


def find_state_path(machine):
	try:
		(state_target, buttons, _) = machine

		queue = deque()

		queue.append((tuple(False for _ in state_target), [], buttons))

		while queue:
			(state, steps, buttons) = queue.popleft()

			print(state_target, state, end='\r')

			if state == state_target:
				return steps

			for (index, button) in enumerate(buttons):
				queue.append((
					tuple(not s if i in button else s for (i, s) in enumerate(state)),
					[*steps, button],
					buttons[index + 1:]
				))
	finally:
		print()


def main():
	count = len(argv) - 1

	assert count <= 2, 'More than two arguments are not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'
	joltage = count >= 2

	process(filename, joltage)


def process(filename, joltage):
	machines = read_file(filename)

	if joltage:
		print(sum((len(find_joltage_path(m)) for m in machines)))
	else:
		print(sum((len(find_state_path(m)) for m in machines)))


def read_file(filename):
	def iterate():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				[state, *buttons, joltage] = line.split()

				state = state.strip('[]')
				buttons = (b.strip('()') for b in buttons)
				joltage = joltage.strip('{}')

				yield (
					tuple(s == '#' for s in state),
					[frozenset(int(l) for l in b.split(',')) for b in buttons],
					tuple(int(j) for j in joltage.split(','))
				)

	return list(iterate())


if __name__ == '__main__':
	main()
