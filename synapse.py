import cons as cons
import weakref

class dendrite(cons.cons_list):
	"""
		one can iterate through a dendrite,
		which has the values from an axon,
		as of the time that the dendrite is made.
		The values are not retained once iterated through.
	"""
	__slots__ = ["_source"]
	def __init__(self,source):
		self._source = source
		super(dendrite,self).__init__(None)
	def next(self):
		try:
			return super(dendrite,self).next()
		except StopIteration:
			self._source.tick()
			return super(dendrite,self).next()

class axon(object):
	"""
		One pushes out values to an axon,
		and one makes dendrites from axons,
		and any existing dendrite can read values from the axon,
		but only the values as of when the dendrite was made,
		and the dendrite can only iterate through those values once.
	"""
	__slots__ = ["_source","_the_cons_list"]
	def __init__(self,source):
		self._the_cons_list = cons.cons_list(None)
		self._source = weakref.ref(source)
	def dendrite(self):
		"make a dendrite"
		result = dendrite(self)
		result._list = self._the_cons_list._list
		return result
	def push(self,item):
		"push a value onto an axon"
		self._the_cons_list.append_and_skip_to(item)
	def tick(self):
		"tell the source that a value should be pushed onto the axon"
		source = self._source()
		if source is None:
			raise StopIteration
		else:
			source.tick()
