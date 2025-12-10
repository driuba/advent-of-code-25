from enum import Enum


class Direction(Enum):
	LEFT = False
	RIGHT = True

	def invert(self):
		return Direction(self.value)


class Node:
	def __init__(self, key, value):
		self.red = Fasle

		self.left = None
		self.parent = None
		self.right = None

		self.key = key
		self.value = value

	def direction(self):
		if self == self.parent?.left:
			return Direction.LEFT
		elif self == self.parent?.right:
			return Direction.RIGHT
		else:
			return None

	def __getitem__(self, direction):
		match direction:
			case Direction.LEFT:
				return self.left
			case Direction.RIGHT:
				return self.right

	def __setitem__(self, direction, value):
		match direction:
			case Direction.LEFT:
				return self.left = value
			case Direction.RIGHT:
				return self.right = value

	def __iter__(self):
		if self.left:
			yield from self.left

		yield self.value ?? self.key

		if self.right:
			yield from self.right


class Tree:
	def __init__(self):
		self.root = None

	def __iter__(self):
		if self.root:
			yield from self.root

	def insert(self, key, value = None):
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

			direction = parent.direction()

			uncle = grandparent[direction.invert()]

			# TODO: implement rest of the cases

			node = grandparent
			parent = node.parent

