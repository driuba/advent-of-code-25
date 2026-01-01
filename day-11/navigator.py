#!/bin/env python3.14t


from collections import deque
from sys import argv


IN = 'svr'
MIDS = ('dac', 'fft')
OUT = 'out'


def count_paths(network, nodes, start, *ends):
	counts = {n: 1 if n == start else 0 for n in network}

	for node in nodes:
		for connection in network[node]:
			counts[connection] += counts[node]

	return tuple((counts[e] for e in ends))


def invert(network):
	network_inverted = {n: set() for n in network}

	for (machine, connections) in network.items():
		for connection in connections:
			network_inverted[connection].add(machine)

	return network_inverted


def main():
	count = len(argv) - 1

	assert count <= 1, 'More than one argument is not supported.'

	filename = argv[1] if count >= 1 else 'input.txt'

	process(filename)


def process(filename):
	network = read_file(filename)

	network_inverted = invert(network)

	nodes = deque()

	while network_inverted:
		for node in [n for (n, cs) in network_inverted.items() if not cs]:
			del network_inverted[node]

			nodes.append(node)

			for connection in network[node]:
				network_inverted[connection].remove(node)

	(a, b) = MIDS

	(count_in_a, count_in_b) = count_paths(network, nodes, IN, a, b)

	(count_a_b, count_a_out) = count_paths(network, nodes, a, b, OUT)

	(count_b_a, count_b_out) = count_paths(network, nodes, b, a, OUT)

	print('The result is', count_in_a * count_a_b * count_b_out + count_in_b * count_b_a * count_a_out)


def read_file(filename):
	def iterate():
		with open(filename) as file:
			for line in file:
				line = line.strip()

				[machine, connections] = line.split(':')

				yield (
					machine.strip(),
					set(connections.strip().split())
				)

			yield ('out', set())

	return {m:cs for (m, cs) in iterate()}


if __name__ == '__main__':
	main()
