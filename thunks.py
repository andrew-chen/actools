from thunk import thunk, accumulator

@thunk
def accumulate():
	result = []
	item = yield
	while True:
		result.append(item)
		item = yield result
@thunk
def summation():
	so_far = yield
	while True:
		so_far += yield so_far
@thunk
def difference(initial=None):
	last = yield
	result = initial
	while True:
		current = yield result
		result = current - last
		last = current
@thunk
def previous(initial = None):
	prev = yield
	result = initial
	while True:
		current = yield result
		result = prev
		prev = current
			
if __name__ == "__main__":
	acc = accumulate()
	#sum = summation()
	sum = accumulator(lambda x,y: x+y,0)
	d = difference()
	p = previous()
	for i in range(10):
		#print acc(i)
		#print d(s(i))
		#print p(i)
		sum(i)
	print sum.last()

