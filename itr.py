from historical_context import HistoricalContext
from collections import deque
import itertools
from acitertools import iter_memo, empty, no_more, needs, last

"""
	A general purpose wrapper around iterables
	
	Between acitertools.py and itr.py,
	all functionality from itertools can be found.

	Intended to provide all the higher order array methods that
	JS and underscoreJS provide.

	.filter() is seen as more general than
		ifilter
			and
		ifilterfalse
			from itertools.
		To get the functionality of ifilterfalse,
			use the Not class from filter.py
"""

# the name of this class is an exception to the convention because
# this is intended to be used as a function of sorts
def itr(iterable,remember_all=False):
	if isinstance(iterable,_itr):
		return iterable
	else:
		return _itr(iterable,remember_all)
		
def count(*args):
	return itr(itertools.count(*args))
		
def repeat(*args):
	return itr(itertools.repeate(*args))
		
class _itr(object):
	"""
		with this, one can do things like:

		for x in itr(iterable).whatever():
			stuff

		rather than having to do:

		for y in interable:
			x = y.whatever()
			stuff

		and the calling of methods in a map() style
		can keep on going
	"""

	def __init__(self,anIterable,remember_all=False):
		"""
			will use iter_memo to ensure that the iterable can restart,
			but allow caller to indicate whether to set remember_all or not
		"""
		self.axon = iter_memo(iter(anIterable),remember_all)
		
		self.iterable = self.axon.__iter__()
	
	def copy(self):
		"""
			copies everything, not just what is left in the iterable,
			if remember_all had been set in the constructor
		"""
		return itr(iter(self.axon.__iter__()))
	
	def __getattr__(self,name):
		return itr(self.getattr_core(name))
	def getattr_core(self,name):
		for item in self.iterable:
			yield getattr(item,name)

	def __getitem__(self,index):
		"""
			slices on self,
			but indexes on elements.
			May want to revisit this.
		"""
		if isinstance(index,slice):
			return itr(itertools.islice(self.iterable,index.start,index.stop,index.step))
		else:
			return itr(self.getitem_core(index))
	def getitem_core(self,index):
		for item in self.iterable:
			yield item[index]

	def __call__(self,*args,**keywords):
		return itr(self.call_core(*args,**keywords))
	def call_core(self,*args,**keywords):
		for item in self.iterable:
			yield item(*args,**keywords)

	def dropwhile(self,pred):
		return itr(itertools.dropwhile(pred,self.iterable))

	def takewhile(self,pred):
		return itr(itertools.takewhile(pred,self.iterable))

	def groupby(self,keyfunc=None):
		return itr(itertools.groupby(self.iterable),keyfunc)

	def tee(self,k=2):
		return tuple(itr(self.axon.dendrite()) for i in range(k))

	def cycle(self):
		return itr(itertools.cycle(self.iterable))

	def enumerate(self):
		return itr(enumerate(self.iterable))
	def numbered(self):
		return self.enumerate()
	
	def permutations(self,r=None):
		return itr(itertools.permutations(self.iterable,r))
	
	def combinations(self,r):
		return itr(itertools.combinations(self.iterable,r))
		
	def combinations_with_replacement(self,r):
		return itr(itertools.combinations_with_replacement(self.iterable,r))
		
		

	def k_wise(self,k):
		return itr(self.k_wise_core(k))
	def k_wise_core(self,k):
		so_far = []
		for item in self.iterable:
			so_far.append(item)
			if len(so_far) == k:
				yield tuple(so_far)
				so_far = []
		if len(so_far) > 0:
			while len(so_far) < k:
				so_far.append(None)
			yield tuple(so_far)

	def filter(self,the_filter=lambda x: x):
		return itr(self.filter_core(the_filter))
	def filter_core(self,the_filter=lambda x: x):
		for item in self.iterable:
			if the_filter(item):
				yield item

	def cross(self,iterable):
		return itr(self.cross_core(iterable))
	def cross_core(self,iterable):
		for x in self.iterable:
			for y in iterable:
				yield (x,y)

	def map(self,the_callable):
		return itr(self.map_core(the_callable))
	def map_core(self,the_callable):
		for item in self.iterable:
			yield the_callable(item)

	def unique(self):
		return itr(self.unique_core())
	def unique_core(self):
		r = set()
		for item in self.iterable:
			if item in r:
				continue
			else:
				r.add(item)
				yield item

	def group_while(self,pred,group_op=lambda x:x):
		return itr(self.group_while_core(pred,group_op))
	def group_while_core(self,pred,group_op):
		iterable = self.iterable
		groups = HistoricalContext(deque)
		for item in iterable:
			if len(groups.current) == 0 or pred(item,groups.current):
				groups.current.append(item)
			else:
				groups.next.append(item)
				group_op(groups.current)
				yield groups.current
				groups.new_next()
		if not empty(groups.current): yield groups.current
			
	def sorted_runs(self,sort_by):
		def sorter(x,y):
			return sort_by(x,last(y))
		return self.group_while(sorter)

	def first(self):
		"just returns the first item"
		for item in self.iterable:
			return item
		# if empty iterable, will raise an error, which is exactly what we want

	def iteriter(self):
		return itr(itertools.chain.from_iterable(self.iterable))

	def iteriteriter(self):
		return itr(self.iteriteriter_core())
	def iteriteriter_core(self):
		iterable = self.iterable
		for item in itertools.chain.from_iterable(iterable):
			for j in item:
				yield j
		
	def pcn_iter(self):
		return itr(self.pcn_iter_core())
	def pcn_iter_core(self):
		"""
			yields triples of (previous,current,next)
			for every item in iterable,
			with None if there is no previous or next
		"""
		iterable = self.iterable
		h = HistoricalContext()
		yielded_anything = False
		for item in iterable:
			h.set_next(item)
			if h.current is not None:
				yield h.pcn_tuple()
				yielded_anything = True
		h.new_next()
		result = h.pcn_tuple()
		(p,c,n) = result
		if c is not None:
			yield result
	
	def merge(self,with_what):
		return itr(self.merge_core(with_what))
	def merge_core(self,with_what):
		"treat them both as sorted iterables and merge them together"
		A = iter(self.iterable)
		B = iter(with_what)
		try:
			a,b = next(A),next(B) # they must have at least one in each
			while True:
				while a < b:
					with needs.A: yield a; a = next(A)
				with needs.B: yield b; b = next(B)
		except no_more.A:
			yield b
			for b in B: yield b
		except no_more.B:
			yield a
			for a in A: yield a

	def balanced_reduce(self,func):
		iterable = self.iterable
		d = deque(iterable)
		while len(d) > 1:
			x,y = d.pop(),d.pop()
			d.appendleft(func(x,y))
		assert(len(d) == 1)
		return d.pop()
	

	def __iter__(self):
		for item in self.iterable:
			yield item

""" this way, we can do the following:

from itr import itr

for x in itr(...).whatever().whatever()...:
	...

"""
if __name__ == "__main__":
	def fib(n):
		if n < 2:
			return n
		else:
			return fib(n-1)+fib(n-2)
	class sFib(object):
		def __init__(self):
			self.im = itr(self).unique()
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
