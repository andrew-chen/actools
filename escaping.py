"""
	General purpose escaping and unescaping
"""
def escape(sentinel,should_escape,iterable):
	for item in iterable:
		if should_escape(item):
			yield sentinel
			yield item
		else:
			yield item

def unescape(sentinel_test,iterable,process_special):
	last_was_sentinel = False
	for item in iterable:
		if last_was_sentinel:
			last_was_sentinel = False
			yield process_special(item)
		else:
			if sentinel_test(item):
				last_was_sentinel = True
			else:
				yield item

class escape_manager(object):
	"""
		Uses escape() and unescape() in a way as to demonstrate that they are inverses
	"""
	def __init__(self,sentinel,should_escape,process_special):
		self.sentinel = sentinel
		self.should_escape = should_escape
		self.process_special = process_special
	def escape(self,iterable):
		return escape(self.sentinel,self.should_escape,iterable)
	def is_sentinel(self,item):
		return (item == self.sentinel)
	def unescape(self,iterable):
		return unescape(self.is_sentinel,iterable,self.process_special)

if __name__ == "__main__":
	e = escape_manager(-1,lambda x: x in [0,1,2,3],lambda x: x)
	l = e.escape(range(10))
	from itertools import tee
	l1,l2 = tee(l)
	print list(l1)
	r = e.unescape(l2)
	print list(r)
