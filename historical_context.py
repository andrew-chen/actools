import declare
from actypes import none

class HistoricalContext(
	declare.initializers(
		previous = none,
		current = none,
		next = none
		)
	):
	def __init__(self,the_default=none):
		super(HistoricalContext,self).__init__()
		self.set_default(the_default)
		self.new_next()
		self.new_next()
		self.new_next()
	def set_default(self,new_default):
		self.default = new_default
	def new_next(self):
		self.set_next(self.default())
	def set_next(self,new_next):
		self.previous = self.current
		self.current = self.next
		self.next = new_next
	def pcn_tuple(self):
		return (self.previous,self.current,self.next)

