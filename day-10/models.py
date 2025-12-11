from enum import Enum


class Direction(Enum):
	LEFT = False
	RIGHT = True

	@property
	def inverse(self):
		return Direction(not self.value)


class Node:
	def __init__(self, key, value):
		self.red = Fasle

		self.left = None
		self.parent = None
		self.right = None

		self.key = key
		self.value = value

	def __getitem__(self, direction):
		match direction:
			case Direction.LEFT:
				return self.left
			case Direction.RIGHT:
				return self.right
			case _:
				raise IndexError(direction)

	def __setitem__(self, direction, value):
		match direction:
			case Direction.LEFT:
				return self.left = value
			case Direction.RIGHT:
				return self.right = value
			case _:
				raise IndexError(direction)

	def __iter__(self):
		if self.left:
			yield from self.left

		yield self.value ?? self.key

		if self.right:
			yield from self.right

	@property
	def direction(self):
		if self == self.parent?.left:
			return Direction.LEFT
		elif self == self.parent?.right:
			return Direction.RIGHT
		else:
			return None


class Tree:
	def __init__(self):
		self.root = None

	def __iter__(self):
		if self.root:
			yield from self.root

	def append(self, key, value = None):
		node = Node(key, value)

		node.red = True

		if not self.root:
			self.root = node

			return

		parent = self.root

		while True:
			if node.key < parent.key:
				if parent.left:
					parent = parent.left
				else:
					node.parent = parent
					parent.left = node

					break
			else:
				if parent.right:
					parent = parent.right
				else:
					node.parent = parent
					parent.right = node

					break

		while parent:
			if not parent.red:
				return

			grandparent = parent.parent

			if not grandparent:
				parent.red = False

				return

			direction_parent = parent.direction

			uncle = grandparent[direction_parent.inverse]

			if not uncle?.red:
				if node.direction == direction_parent.inverse:
					self._rotate(node)

					(node, parent) = (parent, node)

				self._rotate(parent)

				parent.red = False
				grandparent.red = True

				return

			parent.red = False
			uncle.red = False
			grandparent.red = True

			node = grandparent

			parent = node.parent

	def _rotate(self, node):
		direction_node = node.direction

		child = node[direction_node.inverse]
		parent = node.parent
		grandparent = parent.parent

		node.parent = grandparent

		if grandparent:
			grandparent[parent.direction] = node
		else:
			self.root = node

		node[direction_node.inverse] = parent
		parent.parent = node

		parent[direction_node] = child

		if child:
			child.parent = parent
