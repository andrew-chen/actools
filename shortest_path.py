class path(list):
	def start(self):
		return self[0]
	def end(self):
		return self[-1]
	def extend_via(self,list_options):
		for item in list_options(self.end()):
			p = path(self)
			p.append(item)
			yield p
class list_of_paths(list):
	def paths_ending_on(self,which):
		for item in self:
			if item.end() == which:
				yield item
	def extend_via(self,list_options):
		result = list_of_paths()
		for item in self:
			for possibility in item.extend_via(list_options):
				result.append(possibility)
		return result
	def ends(self):
		for item in self:
			yield item.end()
def shortest_paths(start,goal,list_options):
	paths = list_of_paths()

	a_path = path()
	a_path.append(start)
	paths.append(a_path)
	del a_path

	paths_by_distance = [paths]
	del paths

	index = 0
	while True:
		to_consider = paths_by_distance[index]
		new_options = to_consider.extend_via(list_options)
		if len(new_options) == 0:
			raise ValueError, "can not get there from here"
		if goal in new_options.ends():
			for possibility in new_options:
				if goal == possibility.end():
					yield possibility
			return
		else:
			paths_by_distance.append(new_options)
			index += 1

def shortest_path(start,goal,list_options):
	if start == goal:
		return []
	r = list(shortest_paths(start,goal,list_options))
	return r[0]

if __name__ == "__main__":
	def list_options(x):
		return [x+1,x-1,x*2,x/2]
	print list(shortest_paths(5,4,list_options))
	print list(shortest_paths(7,13,list_options))
	print list(shortest_paths(3,13,list_options))

