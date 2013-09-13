import copy

class Decorator(object):
	#__slots__ = ["_0x0123456789x0_"]
	def __init__(self,instance):
		object.__setattr__(self,"_0x0123456789x0_",instance)
	def __getattr__(self,name):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		return getattr(instance,name)
	def __setattr__(self,name,value):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		setattr(instance,name,value)
	def __detattr__(self,name):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		delattr(instance,name)
	def __copy__(self):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		return type(self)(copy.copy(instance))
	def __call__(self,*args,**kwargs):
		return object.__getattribute__(self,"_0x0123456789x0_")(*args,**kwargs)
	def __add__(self,arg):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		if isinstance(arg,Decorator):
			arg = object.__getattribute__(arg,"_0x0123456789x0_")
		return instance+arg
	def __repr__(self,*args,**kwargs):
		instance = object.__getattribute__(self,"_0x0123456789x0_")
		return repr(instance)

if __name__ == "__main__":
	class Test(object):
		def bar(self):
			print "bar"
	class Foo(Decorator):
		def foo(self):
			print "foo"
	b = Foo(Test())
	b.foo()
	b.bar()
	c = copy.copy(b)
	c.foo()
	c.bar()
	class Bar(Decorator):
		def bell(self):
			self.yo = 1
		def bee(self):
			print self.yo
	t = Test()
	d = Bar(Foo(t))
	d.foo()
	d.bar()
	d.bell()
	d.bee()
	print t.__dict__
