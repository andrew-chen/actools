import copy

class cons(object):
	"a lisp-style cons object"
	__slots__ = ["_car","_cdr"]
	def __init__(self,car,cdr):
		"constructor, functions just like cons in lisp"
		self._car = car
		self._cdr = cdr
	def car(self): return self._car
	def first(self): return self._car
	def cdr(self): return self._cdr
	def rest(self): return self._cdr
	def replcar(self,newcar): self._car = newcar
	def replcdr(self,newcdr): self._cdr = newcdr
	def append(self,item):
		result = self
		while result._cdr != None:
			result = result._cdr
		result._cdr = cons(item,None)
		return result._cdr

class cons_list(object):
	"a wrapper around the type of list that can be made from cons objects"
	__slots__ = ["_list"]
	def __init__(self,first_item):
		self._list = cons(first_item,None)
	def append(self,item):
		return self._list.append(item)
	def append_and_skip_to(self,item):
		self._list = self._list.append(item)
	def first(self):
		return self._list.first()
	def rest(self):
		return self._list.rest()
	def next(self):
		"""
			This doesn't return the value of the car ever,
			because it presumes that when first made,
			it will just have None in there,
			as per the constructor.
		"""
		if self._list._cdr != None:
			self._list = self._list._cdr
			return self._list._car
		else:
			raise StopIteration
	def copy(self):
		result = copy.copy(self)
		result._list = self._list
		return result
	def __iter__(self):
		return self

if __name__ == "__main__":
	a = cons_list("a")
	print a.first()
	print a.rest()
	try:
		a.next()
	except:
		print "a.next() was successful"
	b = cons_list("b")
	c = b.copy()
	b.append("c")
	b.append("d")
	b.append("e")
	print b._list
	print c._list
	for item in c:
		print item
	print b._list
	print c._list
	for item in b:
		print item
	print b._list
	print c._list
