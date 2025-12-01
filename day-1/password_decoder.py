#!/bin/env python3.14t

from sys import stderr
from re import compile

expression = compile(r'^(?P<direction>L|R)(?P<value>\d+)$')

value_current = 50
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

		print(value_current, end='\t')

		value = int(match.group('value'))

		rotations = value // 100

		value %= 100
		value *= -1 if match.group('direction') == 'L' else 1

		if value:
			value_old = value_current

			value_current += value

			if value_old and (value_current <= 0 or value_current >=100):
				rotations += 1

			value_current %= 100

		result += rotations

		print(line, value, value_current, rotations, result, sep='\t')

print(result)
