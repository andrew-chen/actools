from functools import wraps, partial, update_wrapper
def thunk(f):
	#a function decorator
	class Thunk(object):
		__slots__ = ["_generator","_initial","_last"]
		def __init__(self,*args,**kwargs):
			self._generator = f(*args,**kwargs)
			self._initial = next(self._generator)
		def __call__(self,arg):
			self._last = self._generator.send(arg)
			return self._last
		def initial(self):
			return self._initial
		def last(self):
			return self._last
	p = partial(Thunk)
	p.__name__ = f.__name__
	p.__doc__ = f.__doc__
	p.__module__ = f.__module__
	return p

@thunk
def accumulator(body,initial_state):
	result = None
	state = initial_state
	while True:
		result = body(state, (yield result))
		state = result
