def none():
	"""
		a constructor for None
	"""
	return None

class Callbacker(object):
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
		
		Accepts a proxy as an argument, which has .set(value) and .get() methods
		
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
