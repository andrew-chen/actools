# this is designed to support arbitrary hierarchical ordered data structures
# they have children that are ordered
# properties are not children
# designed to support subclassing/factories/combinations_thereof

import copy

class Base(object):
	def __init__(self):
		super(Base,self).__init__()
	def is_parent(self):
		return 0
	def is_leaf(self):
		return 0

class Container(Base):
	def __init__(self):
		super(Container,self).__init__()
		self._children = []
	def is_parent(self):
		return 1
	def __getitem__(self,key):
		return self._children[key]
	def __setitem__(self,key,value):
		self._children[key] = value
	def __len__(self):
		return len(self._children)
	def append(self,item):
		self._children.append(item)
	def append_items(self,items):
		for item in items:
			self.append(item)
	def children(self):
		" lets us iterate through the children "
		# we make a copy first to allow predictable behavior
		# if the list of children are being altered during this
		kids = copy.copy(self._children)
		for kid in kids:
			yield kid
	def leaves(self):
		" lets us iterate through the descendant leaves "
		for child in self.children():
			if child.is_parent():
				for leaf in child.leaves():
					yield leaf
			else:
				yield child
				

class Leaf(Base):
	def __init__(self):
		super(Leaf,self).__init__()
	def is_leaf(self):
		return 1
