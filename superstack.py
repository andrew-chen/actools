"""
	Provides stuff useful for many common stack use cases
"""
from collections import deque
from itr import itr
class Stack(object):
	def __init__(self):
		self._stack = deque()
	def __str__(self):
		return repr(self._stack)
	def top(self):
		return self._stack[-1]
	def pop(self):
		return self._stack.pop()
	def push(self,item):
		self._stack.append(item)
	def pop_while(self,condition):
		result = []
		while not self.empty() and condition(self.top()):
			result.append( self.pop() )
		print(result)
		return itr(result)
	def pop_while_and_including(self,condition):
		result = []
		while not self.empty() and condition(self.top()):
			result.append( self.pop() )
		result.append(self.pop())
		return itr(result)
	def pop_while_but_not_last(self,condition):
		result = []
		while not self.empty() and condition(self.top()):
			result.append( self.pop() )
		last = result[-1]
		self._stack.append(last)
		return itr(result[:-1])		
	def pop_just_beyond(self,condition):
		result = []
		while not self.empty() and condition(self.top()):
			result.append( self.pop() )
		try:
			result.append(self.pop())
		except IndexError:
			print("IndexError in pop_just_beyond")
			raise
		return itr(result)
	def pop_all(self):
		return self.pop_while(lambda x: True)
	def any(self,condition):
		for item in self._stack:
			if condition(item):
				return True
		return False
	def all(self,condition):
		for item in self._stack:
			if not condition(item):
				return False
		return True
	def empty(self):
		return 0 == len(self._stack)
	def contents(self):
		return list(self._stack)

class CommonStack(Stack):
	"""
		Assumes all elements are (type,value)
	"""
	def push(self,Type,Value):
		super(CommonStack,self).push((Type,Value),)
	def type_pop_while(self,condition):
		def cond_func(arg):
			return condition(arg[0])
		return self.pop_while(cond_func)
	def type_pop_while_and_including(self,condition):
		def cond_func(arg):
			return condition(arg[0])
		return self.pop_while_and_including(cond_func)
	def type_pop_just_beyond(self,condition):
		def cond_func(arg):
			return condition(arg[0])
		return self.pop_just_beyond(cond_func)
	def value_pop_while(self,condition):
		def cond_func(arg):
			return condition(arg[1])
		return self.pop_while(cond_func)
	def pop_until_type(self,Type):
		def cond_func(arg):
			return arg != Type
		return self.type_pop_while(cond_func)
	def pop_until_and_including_type(self,Type):
		def cond_func(arg):
			return arg != Type
		return self.type_pop_while_and_including(cond_func)
	def pop_until_just_beyond_type(self,Type):
		def cond_func(arg):
			return arg != Type
		return self.type_pop_just_beyond(cond_func)
	def pop_value_until_type(self,Type):
		return self.pop_until_type(Type)[1]
	def pop_value_until_and_including_type(self,Type):
		return self.pop_until_and_including_type(Type)[1]
	def pop_value_until_just_beyond_type(self,Type):
		if self.has_type(Type):
			return self.pop_until_just_beyond_type(Type)[1]
		else:
			print("Tried to pop until just beyond type "+str(Type)+" but such type not present")
			raise
	def _pop_value_while_type(self,condition):
		def cond_func(arg):
			return condition(arg[0])
		for (t,v) in self.pop_while(cond_func):
			yield v
	def pop_value_while_type(self,condition):
		return itr(self._pop_value_while_type(self))
	def pop_value(self):
		r = self.pop()
		return r[1]
	def top_type(self):
		r = self.top()
		return r[0]
	def top_value(self):
		r = self.top()
		return r[1]
	def value_pop_all(self):
		r = self.pop_all()
		return r[1]
	def has_type(self,Type):
		def cond_func(arg):
			return arg[0] == Type
		return self.any(cond_func)
	def all_values(self):
		result = []
		for (t,value) in self.contents():
			result.append(value)
		return result


	
