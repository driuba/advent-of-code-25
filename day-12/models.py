from enum import Enum, EnumMeta


class _DirectionMeta(EnumMeta):
	def __call__(cls, value):
		if isinstance(value, str):
			value = value.lower()

		return super().__call__(value)


class Direction(Enum, metaclass=_DirectionMeta):
	DOWN = 'down'
	LEFT = 'left'
	RIGHT = 'right'
	UP = 'up'

	def __invert__(self):
		match self:
			case Direction.DOWN:
				return Direction.UP
			case Direction.LEFT:
				return Direction.RIGHT
			case Direction.RIGHT:
				return Direction.LEFT
			case Direction.UP:
				return Direction.DOWN
			case _:
				raise ValueError()


def Graph:
	def __init__(self):
		self._nodes = []


class Node:
	def __init__(self, id = None, tag = None):
		self._connections = {}
		self._id = id
		self._tag = tag

	def __contains__(self, direction):
		direction = Direction(direction)

		return direction in self._connections;

	def __getitem__(self, direction):
		direction = Direction(direction)

		assert direction in self

		return self._connections[direction]

	def __setitem__(self, direction, node):
		direction = Direction(direction)

		assert isinstance(node, Node)
		assert direction not in self
		assert ~direction not in node

		self._connections[direction] = node
		node._connections[~direction] = self

	def __delitem__(self, direction):
		dirction = Direction(direction)

		node = self[direction]

		del self._connections[direction]
		del node._connections[~direction]

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
		self._id = id

	@id.deleter
	def id(self):
		del self._id

	@property
	def tag(self):
		return self._tag

	@tag.setter
	def tag(self, tag):
		self._tag = tag

	@tag.deleter
	def tag(self):
		del self._tag
