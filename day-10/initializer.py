#!/bin/env python3.14t


from collections import deque
from sys import argv


def find_path(machine):
	(state_target, buttons, _) = machine

	queue = deque()

	queue.append((tuple(False for _ in state_target), [], buttons))

	while len(queue):
		(state, steps, buttons) = queue.popleft()

		if state == state_target:
			return steps

		for (index, button) in enumerate(buttons):
			queue.append((
				tuple(not s if i in button else s for (i, s) in enumerate(state)),
				[*steps, button],
				buttons[index + 1:]
			))


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	machines = read_file(filename)

	print(sum((len(find_path(m)) for m in machines)))


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
