from creating import AttributeFactory, ItemFactory
from functools import wraps

class OutermostExit(object):
	"""
		The general idea behind this class is that,
		when an object might have nested context managers associated with it,
		and when the closing action only needs to be done at
		the close of the outermost,
		this is used to register the closing action,
		and also,
		that a single one of these is made for each such object.
	"""
	def __init__(self,atexit):
		self.atexit = atexit
		self.count = 0
	def __enter__(self):
		self.count += 1
		return self
	def __exit__(self,exc_type, exc_val, exc_tb):
		self.count -= 1
		if self.count == 0: self.atexit()
		return False

class SubstituteException(object):
	"""
		allows the substitution of one exception with another,
		useful for having different exception handlers
		if the same block of code could generate the same exception,
		but for different reasons,
		and there would be need to do different things based on the reason
	"""
	def __init__(self,exception,by):
		self.the_exception = exception
		self.to_be_raised = by
	def __enter__(self):
		return self
	def __exit__(self,exc_type, exc_val, exc_tb):
		if exc_type is None:
			return False
		if isinstance(exc_type,self.the_exception):
			raise self.to_be_raised, exc_val
		if issubclass(exc_type,self.the_exception):
			raise self.to_be_raised, exc_val
		return False

#the following classes are for handling exceptions in the initial part of a func
class InitialBlock_(Exception):
	"""
		The class for exceptions within the initial block,
		and this also makes subclasses of itself for
		all other exception types as necessary
	"""
	@classmethod
	def _of(cls,exc_type):
		try:
			children = cls.children
		except:
			cls.children = {}
			children = cls.children
		if children.has_key(exc_type):
			return children[exc_type]
		else:
			class InitialBlock(exc_type,InitialBlock_):
				def base_exception_type(self):
					return exc_type
			cls.children[exc_type] = InitialBlock
			return cls.children[exc_type]

class _initial_block(object):
	"""
		In a function there's usually an initial setup section,
		and exceptions that occur then should usually be handled differently
		than exceptions that occur in the rest.
		
		This helps with that.
	"""
	def __init__(self):
		pass
	def __enter__(self):
		return self
	def __exit__(self,exc_type, exc_val, exc_tb):
		if exc_type is None:
			return False
		raise InitialBlock_._of(exc_type), exc_val

initial_block = _initial_block()

def has_initial_block(f):
	"""
		A function decorator that catches all
		"initial" exceptions and transforms them back to their
		"normal" forms when leaving the function
	"""
	@wraps(f)
	def the_func(*args,**kwargs):
		try:
			return f(*args,**kwargs)
		except InitialBlock_ as e:
			raise e.base_exception_type(e.args)
	return the_func

class Initial_Exception(SubstituteException):
	"""
		This substitutes ordinary exceptions for the corresponding
		"initial" equivalent of them
	"""
	def __init__(self,what):
		exc_type = what
		super(Initial_Exception,self).__init__(
			exc_type,
			InitialBlock_._of(exc_type)
			)

initial = ItemFactory(Initial_Exception)

# the above should all be able to work like this
"""
@has_intial_block
def ...
	try:
		with initial_block:
			...
		while True:
			...
	except initial[Whatever]:
		...
	except Whatever:
		...
	
"""


class ignoring_all(object):
	def __enter__(self):
		return self
	def __exit__(self, exc_type, exc_val, exc_tb):
		return True

global ignoring
ignoring = ignoring_all()

if __name__ == "__main__":
	with ignoring:
		open("/////../../..")	
	with SubstituteException(IOError,by=StopIteration):
		open("/////../../..")

