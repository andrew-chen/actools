import creating
import actypes

def initializers(**keywords):
	"""
		function that returns a class,
		and the class is intended as a base class,
		and so the intent is that the function call be in the
		declaration of the base class
		
		function call arguments are keyword arguments,
		that associate a name with a callable (usually a class),
		and when an attribute with that name is accessed,
		but doesn't yet exist, the callable is called to
		return the value that the attribute should be populated with.
		
		In addition to the builtin types and classes,
		see actypes.py for some others.
	"""
	class _base(object):
		def __getattr__(self,name):
			if keywords.has_key(name):
					result = keywords[name]()
					setattr(self,name,result)
					return result
			try:
				return super(_base,self).__getattr__(name)
			except AttributeError:
				err_msg = "instance {0:#x} of {1} has no attribute {2}".format(id(self),self.__class__.__name__,name)
				raise AttributeError, err_msg
	return _base

def initializer(**keywords):
	"""synonym for initializers"""
	return initializers(**keywords)

def values(**args):
	"""
		function that returns a class,
		and the class is intended as a base class,
		and so the intent is that the function call be in the
		declaration of the base class
		
		function call arguments are keyword arguments,
		that associate a name with a value,
		and when an attribute with that name is accessed,
		but doesn't yet exist, the value is used to
		provide the value that the attribute should be populated with.
	"""
	class _obj(object):
		def __init__(self):
			for item in args.keys():
				setattr(self,item,args[item])
			super(_obj,self).__init__(self)
	return _obj

def value(**args):
	return values(**args)

# inheriting from both initializers and values enables you to both set
# lazily evaluated values in base _and_ set actual values in obj
#
# example
# import declare
# class Whatever(
#	declare.initializers(
#		time=now
#	),
#	declare.values(
#		count=0
#	)
# ):
#	and then the actuall class definition
#

def supports(**keywords):
	"""
		keyword arguments are names of interfaces the object claims to support
		and values are either 1 or 0 to indicate if it claims
		to be or not to be
		supporting the interface in question
	"""
	method_names = {}
	for key in keywords:
		method_names["is_"+key] = keywords[key]
	class claimer(object):
		def __getattr__(self,name):
			try:
				return actypes.Variable(method_names[name])
			except:
				return super(claimer,self).__getattr__(name)
	return claimer


def _test_for(name):
	"""
		returns a function that tests to see if
			the argument has an is_*** method
		and
			if it returns a true value
		if it doesn't have that method, or if it doesn't return a true value,
			then this returns a false value,
			otherwise a true value
	"""
	def result(obj):
		methodName = "is_"+name
		try:
			f = getattr(obj,methodName)
			r = f()
			if r:
				return True
			else:
				return False
		except:
			return False
	return result

global test_for
test_for = creating.AttributeFactory(_test_for)

def requirer_helper(arg,item):
	"tests to see if item passes arg"
	try:		
		if type(arg) == type(""):
			is_func = _test_for(arg)
			if is_func(item):
				pass
			else:
				return False
		else:
			for i in arg:
				if requirer_helper(arg,item):
					pass
				else:
					return False		
	except:
		try:
			if isinstance(item,arg):
				pass
			elif issubclass(item,arg):
				pass
			else:
				return False
		except:
			pass
	return False
			
def requires(**keywords):
	"""
		keyword arguments are names of attributes
			that the returned class will intercept
		and their values are things that those must be,
			as follows:
				if a string, must return true to is_***
				if a class, must pass isinstance
				if a list, must be true for all elements in it
				
		TODO:
				add
					"if a set, must be equal to an element of it" (Pascal/C style enum)
					"if an instance of passes(), passing the item through that function must return True"
						has this replace the string-based must_return_true_to_ is_ 
	"""
	class requirer(object):
		def __setattr__(self,name,value):
			invoke_super = False
			raise_error = False
			try:
				v = keywords[name]
				if requirer_helper(v,value):
					invoke_super = True
				else:
					raise_error = True
			except:
				invoke_super = True
			if raise_error:
				raise ValueError, "violation of requires"
			if invoke_super:
				super(requirer,self).__setattr__(name,value)
	return requirer
