class dummy_object(object):
	"""
		a dummy object
		
		when we want an object, but we don't care about assigning any methods to it
	"""
	pass

def none():
	"""
		a constructor for None
	"""
	return None

class Callbacker(object):
	"""
		A class that can have its instances be weakly referenced,
		and which more importantly has the ability to set,get, and call a callback
	"""
	__slots__ = ["__weakref__","_callback"]
	def get_callback(self):
		try:
			return self._callback
		except:
			return None
	def set_callback(self,callback):
		self._callback = callback
	def call_callback(self,old_value,new_value):
		r = self.get_callback()
		if r is None:
			pass
		else:
			r(self,old_value,new_value)

class Variable(Callbacker):
	"""
		A very simple class that has a value and that is it
		
		It calls a callback whenever the value changes
	"""
	__slots__ = ["value"]
	def __init__(self,value):
		self.value = value
	def __call__(self):
		return self.value
	def set(self,value):
		old_value = self.value
		self.value = value
		self.call_callback(old_value,value)

class Proxy(Callbacker):
	"""
		A "Proxy" class, that saves and object and an attribute,
		and has set and get that work on that attribute of that object,
		and calls the callback whenever it is set
	"""
	__slots__ = ["obj","attr"]
	def __init__(self,obj,attr):
		self.obj = obj
		self.attr = attr
	def get(self):
		return getattr(self.obj,self.attr)
	def set(self,value):
		setattr(self.obj,self.attr,value)
		self.call_callback(self.get(),value)

class TidyAssign(object):
	"""
		Remembers previous value,
		Functions as a context manager.
		
		Accepts a Proxy as an argument, which has .set(value) and .get() methods
		
		Motivated by the code in iotools.py
		
		Doesn't need to inherit from Callbacker because
		proxy will callback as necessary
	"""
	def __init__(self,proxy,new_value):
		self.proxy = proxy
		self.new_value = new_value
	def __enter__(self):
		self.old_value = self.proxy.get()
		self.proxy.set(self.new_value)
		return self.new_value
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.proxy.set(self.old_value)
		return False

class CloneableObject(object):
	"""
		supports a clone method that copies all attributes over to the cloned copy
		
		subclasses must support default __init__ methods
	"""
	def clone(self,**kwargs):
		the_class = self.__class__
		the_instance = the_class()
		for key,val in self.__dict__.items():
			setattr(the_instance,key,val)
		for key,val in kwargs.items():
			if val is None:
				pass
			else:
				setattr(the_instance,key,val)
		return the_instance
		