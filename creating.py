class AttributeFactory(object):
	"""
		An attribute factory
			is something that creates something
			just based on accessing an attribute of it
	"""
	__slots__ = ["factory"]
	def __init__(self,theRealFactory):
		self.factory = theRealFactory
	def __getattr__(self,name):
		return self.factory(name)

class ItemFactory(object):
	"""
		An item factory
			is something that creates something
			just based on accessing an item of it
	"""
	__slots__ = ["factory"]
	def __init__(self,theRealFactory):
		self.factory = theRealFactory
	def __getitem__(self,item):
		return self.factory(item)
