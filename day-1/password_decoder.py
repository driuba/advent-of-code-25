#!/bin/env python3.14t

from sys import stderr
from re import compile

expression = compile(r'^(?P<direction>L|R)(?P<value>\d+)$')

current = 50
result = 0

with open('./input.txt') as file:
	for line in file:
		line = line.strip()

		if not line:
			continue

		match = expression.match(line)

		if not match:
			print(f'Umatched line {line}', file=stderr)

			continue

		value = int(match.group('value'))
		value *= -1 if match.group('direction') == 'L' else 1

		current += value
		current %= 100

		if current == 0:
			result += 1

print(result)
