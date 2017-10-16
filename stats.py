"""
	a statistics class
	
	which statistics? they're defined separately as coroutines and passed in as a list in the constructor call
	
	advantages:
		feed the the values as you get them
		only calculates the statistics you need
		extendible to support new statistics
		efficient: does not store the history of everything fed to it, unless an extension does
		convenient syntax compared to reimplementing it
		statistics and be based on other statistics and will calculate them in the correct order

	syntax:
	
		to access another feature (x)'s value:
			self.x
			
		to declare a feature:
			@feature
			def whatever(self):
			
		to have that feature:
			stats = statistics(features=[sum,count,...])
			
		to feed in an item:
			stats(item)
			
		to indicate done:
			stats.done()
			
		to use with an iterator and transformation function:
			map(stats,items) # to transform, do map(stats,map(transform,items))
			stats.done()
			return (stats.mean,stats.stddev,...)
			
			
		to declare that a feature needs other features:
			@feature(needs=[average,history])
			def stddev(self):
			
			# although I think there is an efficient way to calculate stddev without needing history
		
		to indicate that a feature will no longer be needed:
			del statsobj.x
				or
			del self.x
			# would override __delattr__, calling super() if the attribute isn't one of the features
			# would need a dictionary that maps the features name to a reference count,
			# which would be set to one initially and then each "need" would increment,
			# and each del would decrement
"""

import acsetup
import acedu

from thunk import thunk

def feature(*args,**kwargs):
	if len(args) == 1:
		if len(kwargs) == 0:
			name = args[0].__name__
			result = thunk(args[0])
			result.__name__ = name
			result.needs = []
			return result
		else:
			raise TypeError("either takes no arguments, or one keyword argument")
	else:
		if len(kwargs) == 1:
			if kwargs.has_key("needs"):
				def _func(func):
					func.needs = kwargs["needs"]
					result = thunk(func)
					result.__name__ = func.__name__
					result.needs = func.needs
					return result
				return _func
			else:
				raise TypeError("either takes no arguments, or one keyword argument of 'needs'")
		else:	
			raise TypeError("either takes no arguments, or one keyword argument")

from collections import defaultdict

@feature
def count(self):
	result = 0
	item = yield
	while True:
		result += 1
		item = yield result

@feature
def sum(self):
	result = 0
	item = yield
	while True:
		result += item
		item = yield result

@feature(needs=[count,sum])
def average(self):
	first = yield
	while True:
		yield self.sum/self.count

# All the features should be thunks - will be the most natural way to implement them,
# and this way each can retain whatever state they need

# Need to implement the @feature(needs=[...]) support in the decorator, so need to implement something slightly different than what thunk implements, but really close

# WORK HERE

class statistics(object):
	def __init__(self,features):
		self.ordered_features = list()
		self.features = dict()
		self.retained = defaultdict(lambda:0)
		self.feature_values = dict()
		for feature in features: 
			self._install_feature(feature)
	def _install_feature(self,the_feature):
		name = the_feature.__name__
		self.retained[name] += 1
		if name in self.ordered_features:
			return
		feature = the_feature(self)
		self.features[name]=feature
		the_needs = []
		try:
			the_needs = the_feature.needs
		except AttributeError: # in case "the_feature" doesn't have a ".needs" part
			pass
		for needed in the_needs:
			self._install_feature(needed)
		# ensures we add this one to the end of the list before we add any others
		self.ordered_features.append(name)
				
	def __call__(self,item):
		try:
			of = self.ordered_features
		except AttributeError:
			raise ValueError("called stats to process another item after it was told there would be no more items")
		for key in of:
			self.feature_values[key] = self.features[key](item)
	def done(self):
		del self.features
		del self.retained
		del self.ordered_features
	def __getattr__(self,name):
		if name in self.features.keys():
			try:
				return self.feature_values[name]
			except KeyError:
				print "attempted to access value of a feature, but the feature does not have any values yet (likely average with an empty list"
				raise
		super(statistics,self).__getattr__(name)
	def __delattr__(self,name):
		try:
			feature = self.features[name] 
		except AttributeError:
			super(statistics,self).__delattr__(name)
			return
		self.retained[name] -= 1
		if self.retained[name] < 1:
			del self.features[name]
			del self.retained[name]
			del self.feature_values[name]
			self.ordered_features.remove(name)
			try:
				the_needs = feature.needs
			except AttributeError:
				return
			for needed in the_needs:
				self.retained[needed] -= 1
				if self.retained[needed] <= 0:
					self.__delattr__(needed.__name__)

if __name__ == "__main__":
		s = statistics(features=[average])
		map(s,range(10))
		print s.average