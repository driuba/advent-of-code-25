from heapq import heapify, heappop, heappush


class Heap:
	def __init__(self):
		self.values = []

		heapify(self.values)

	def __contains__(self, item):
		return item in self.values

	def __len__(self):
		return len(self.values)

	def pop(self):
		item = heappop(self.values)

		if not item.values:
			return item.key

		return (item.key, *item.values)

	def push(self, key, values):
		heappush(self.values, Node(key, values))


class Node:
	def __init__(self, key, *values):
		self.key = key
		self.values = values

	def __lt__(self, other):
		return self.key < other.key

	def __le__(self, other):
		return self.key <= other.key

	def __ge__(self, other):
		return not self < other

	def __gt__(self, other):
		return not self <= other

	def __eq__(self, other):
		return self._value == other._value

	def __hash__(self):
		return hash(self._value)

	@property
	def _value(self):
		return self.key if self.values else self.values[0]

