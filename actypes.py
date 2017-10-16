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

def true():
	"""
		a constructor for True
	"""
	return True

def false():
	"""
		a constructor for False
	"""
	return False

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
		
		TODO:
			make utility function so usage syntax is:
				with tidy_assign(object,attr=val):
					...
			and thus the need to explicitly make this class or proxy is limited
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

def tidy_assign(obj,**kwargs):
	"""
		TODO:
			expand to support multiple kwargs, not just be limited to one
			OR
			explain why that isn't something that I'll be doing (more likely)
	"""
	assert(1==len(kwargs))
	p = Proxy(obj,kwargs.keys()[0])
	result = TidyAssign(p,kwargs.values()[0])
	return result

class CloneableObject(object):
	"""
		supports a clone method that copies all attributes over to the cloned copy
		
		subclasses must support default __init__ methods
			or override _create()
			or pass any __init__ args into clone before the keyword args
	"""
	def _create(self,*args,**kwargs):
		the_class = self.__class__
		the_instance = the_class(*args)
		return the_instance
	def _transform(self,key,val):
		return val
	def clone(self,*args,**kwargs):
		the_instance = self._create(*args)
		for key,val in self.__dict__.items():
			setattr(the_instance,key,self._transform(key,val))
		for key,val in kwargs.items():
			if val is None:
				pass
			else:
				setattr(the_instance,key,self._transform(key,val))
		return the_instance
		
class DictAdaptor(CloneableObject):
	"""
		__init__ takes in keyword arguments of dictionary names,
		and then from_dict clones and adapts those names from that dict 
	"""
	def __init__(self,*args,**kwargs):
		"must work if nothing in kwargs as per the CLoneableObject interface"
		if len(kwargs):
			self._dict_adaptor_info = kwargs
		try:
			super(DictAdaptor,self).__init__(*args)
		except TypeError:
			pass # if none of the above classes in the hierarchy handle arguments, then we don't know to invoke super here so we don't
	def from_dict(self,the_dict):
		result = self.clone()
		for key,val in self._dict_adaptor_info.items():
			try:
				setattr(result,key,the_dict[val])
			except:
				raise
		return result

class DictAdaptorAuto(DictAdaptor):
	"""
		like DictAdaptor, but from_dict 
	"""

class CloneableWithCopyOptions(CloneableObject):
	"""
		since we may want to deepcopy some attributes or not copy some others,
		this allows us the flexibility to specify which for which attribute
	"""
	def __init__(self,*args,**kwargs):
		self._copy_options = kwargs
		super(CloneableWithCopyOptions,self).__init__(*args)
	def _transform(self,key,val):
		try:
			return self._copy_options[key](val)
		except KeyError:
			return val

"""
	If we were to subclass from both DictAdaptor and CloneableWithCopyOptions,
	we would need to have kwargs be a dict of pairs and then transform the dict of pairs into a pair of dicts,
	and then pass each dict into the respective superclass.
	
	Need utilities that transform dicts of pairs into pairs of dicts and vice versus
"""