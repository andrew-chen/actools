def invert_options_func(start,options_func):
	data = []
	for item in options_func(start):
		data.append((start,item),)
	changed = 1
	while changed:
		changed = 0
		for s,t in data:
			for item in options_func(t):
				if (t,item) not in data:
					data.append((t,item),)
					changed = 1
	def inverted_helper(x):
		for item in data:
			if item[1] == x:
				yield item[0]
	def inverted(x):
		return list(inverted_helper(x))
	return inverted

if __name__ == "__main__":
	def options_func(x):
		u = (x+1)%10
		d = (x-2)%10
		return [u,d]
	inverted = invert_options_func(0,options_func)
	for i in range(10):
		print i,inverted(i)
