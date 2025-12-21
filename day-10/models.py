from heapq import heapify, heappop, heappush


class Heap:
	def __init__(self):
		self.values = []

		heapify(self.values)

	def __len__(self):
		return len(self.values)

	def pop(self):
		item = heappop(self.values)

		if not item.values:
			return item.key

		return (item.key, *item.values)

	def push(self, key, *values):
		heappush(self.values, _Node(key, *values))


class _Node:
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
		return self.key == other.key

	def __hash__(self):
		return hash(self.key)

