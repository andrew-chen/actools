"""
	Between acitertools.py and itr.py,
	all functionality from itertools can be found.
	
	In general, if something in itertools
		creates an iterable with no iterable argument,
			then it is in itr
		takes a single iterable argument,
			then it is in itr
		takes an unspecified arbitrary number of iterables as arguments,
			then it is in itr
		takes a finite number of iterables as arguments,
			then it is in acitertools,
"""

from historical_context import HistoricalContext
from collections import deque
import creating
import exceptiontools
import synapse
import copy
import itertools

def last(a_list):
	"returns the last element in the list"
	return a_list[-1]

def empty(a_list):
	"returns if empty"
	return not len(a_list)

def compress(*args):
	return itertools.compress(*args)

def imap(*args):
	return itertools.imap(*args)

def starmap(*args):
	return itertools.starmap(*args)

def izip(*args):
	return itertools.izip(*args)

def izip_longest(*args):
	return itertools.izip_longest(*args)

def product(*args):
	return itertools.product(*args)




def pairs_of(iterable):
	return itertools.combinations(iterable,r=2)

def numbered(iterable):
	return enumerate(iterable)
	
def iteriter(iterable):
	return itertools.chain.from_iterable(iterable)

def pad_with(iter1,iter2):
	count = 0
	iter1 = iter(iter1)
	iter2 = iter(iter2)
	for item in iter1:
		yield item
		count += 1
	while True:
		if count > 0:
			next(iter2)
			count -= 1
		else:
			yield next(iter2)

class tuple_to_dict_with_defaults(object):
	def __init__(self,names,defaults):
		self.names = names
		self.defaults = defaults
	def __call__(self,the_tuple):
		values = pad_with(the_tuple,self.defaults)
		t = iter_tuple(self.names,values)
		return {key:value for (key,value) in t}

def pairs_to_dict_with_defaults(*args):
	args=list(args)
	args.reverse()
	args.append((None,None),) # because the first item is consumed by tuple_iter
	args.reverse()
	r = tuple_iter(args)
	names,defaults = r()
	names = list(names)
	defaults = list(defaults)
	return tuple_to_dict_with_defaults(names,defaults)


def iter_tuple(*args):
	"""
		takes iterators and make a single iterator that has tuples,
		where the elements of the tuple are from those iterators
	"""
	args = map(iter,args)
	while True:
		result = []
		for item in args:
			result.append(next(item))
		yield tuple(result)

class tuple_iter(object):
	"""
		takes an iterator of tuples.
		__call__ returns a tuple of iterators.
		The first item of the iterator is called at construction time,
		to determine how many iterators to make,
		and that first item is not part of what is returned.
	"""
	def __init__(self,arg):
		self._iterator = iter(arg)
		self._first = next(self._iterator)
		self._count = len(self._first)
		self._axons = [synapse.axon(self) for i in range(self._count)]
		for i, item in enumerate(self._first):
			self._axons[i].push(item)
			
	def __call__(self):
		return tuple(map(lambda x: x.dendrite(),self._axons))

	def tick(self):
		for i, item in enumerate(next(self._iterator)):
			self._axons[i].push(item)
	

def iter_k(iterable,k):
	"""
		similar to itertools.chain.from_iterable(iterable)
		except will go down k levels
	"""
	if k < 1:
		yield iterable
	elif k == 1:
		for item in iterable:
			yield item
	else:
		for outer_item in iterable:
			for inner_item in iter_k(outer_item,k-1):
				yield inner_item

def iter_star(iterable):
	"""
		assume everything is an iterable,
		and yield only those that aren't
	"""
	try:
		for item in iterable:
			for j in iter_star(item):
				yield j
	except:
		yield iterable


class No_More_(Exception):
	"""
		When the lack of an additional iterator should actually raise an exception,
		and not StopIteration
	"""
	@classmethod
	def _of(cls,name):
		try:
			children = cls.children
		except:
			cls.children = {}
			children = cls.children
		if children.has_key(name):
			return children[name]
		else:
			class SpecificNoMore(No_More_):
				def get_name(self):
					return name
			cls.children[name] = SpecificNoMore
			return cls.children[name]

class Needs(exceptiontools.SubstituteException):
	def __init__(self,what):
		super(Needs,self).__init__(StopIteration,No_More_._of(what))

needs = creating.AttributeFactory(Needs)

no_more = creating.AttributeFactory(No_More_._of)

# Using the above, can write the code that assumes all is available,
# and then use exception handling to deal with when it isn't
# see mergesort.py for an example

# the entire rest of this file can be rewritten to be more elegant,
# and perhaps should be put into another file


class iter_memo(synapse.axon):
	"""
		it wraps another iterator,
		and remembers the values returned from it,
		and can return them for it,
		thus serving as a caching proxy for it,
		
		nothing is ever purged from the cache if remember_all is True,
		otherwise, it only remembers what it needs to for existing iterators,
		and new ones only get what will be added just after this

		an iterator that can have things pushed onto it,
		or pulled from it

		this was intended for the sort of scenario where,
		for example, as you read things, you may
		encounter a reference to something not yet defined,
		so you could read along further until you found it,
		and along the way, other things might get defined.

		getting the next definition is "pull",
		but along the way, one might "push" other definitions in
	"""
	def __init__(self,iterable,remember_all=False):
		self.iterable = iterable.__iter__()
		super(iter_memo,self).__init__(self)
		self.remember_all = remember_all
		if self.remember_all:
			self.all = self.dendrite()
	def __iter__(self):
		if self.remember_all:
			return copy.copy(self.all)
		else:
			return self.dendrite()
	def source(self):
		s = self._source()
		if s is None:
			raise StopIteration
		else:
			return s
	def tick(self):
		self.push(next(self.iterable))

# iter_memo_unique is replaced with itr.itr(iterable).unique()

if __name__ == "__main__":
	def fib(n):
		if n < 2:
			return n
		else:
			return fib(n-1)+fib(n-2)
	class sFib(object):
		def __init__(self):
			self.im = iter_memo(self)
		def __iter__(self):
			a = 0
			b = 1
			yield b
			while 1:
				a = a+b
				yield a
				b = a+b
				yield b

		def iterator(self):
			for r in self.im:
				yield r
	s = sFib()
	j0 = s.iterator()
	for i in range(10):
		j1 = next(j0)
		j2 = fib(i+1)
		print (j1,j2)

	stuff = iter_memo(iter_tuple([0,1,2],["A","B","C"],["a","b","c"]),remember_all=True)
	print list(stuff)
	print list(stuff)
	
	tio = tuple_iter(stuff)
	
	n,L,l = tio()

	if 0:	
		print n
		print L
		print l
	
	for _n in n:
		print _n
	for _L in L:
		print _L
	for _l in l:
		print _l
