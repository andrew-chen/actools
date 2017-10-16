from collections import deque
def bfs(to_traverse,get_children):
	so_far = deque()
	them = set()
	yield to_traverse
	so_far.append(to_traverse)
	them.add(to_traverse)
	while len(so_far):
		item = so_far.popleft()
		children = get_children(item)
		for child in children:
			if child not in them:
				yield child
				so_far.append(child)
				them.add(child)

if __name__ == "__main__":
	stuff = frozenset([frozenset([frozenset([1,2,3]),frozenset([4,5])]),frozenset([6,7,8,9])])
	for item in bfs(stuff,lambda x: x if hasattr(x,"__iter__") or hasattr(x,"__len__") else []):
		print item
