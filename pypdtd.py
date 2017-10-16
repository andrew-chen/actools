import acsetup
import copy
import bfs
import hiertext
import shortest_path
import invert_options_func

class _node(hiertext.TextContainer):
	@staticmethod
	def can_be_within(other):
		return False
	@staticmethod
	def is_root():
		return False
	@staticmethod
	def those_can_be_within():
		return []

	def should_clear(self):
		return True
		
	def list_nodes(self,type):
		for item in self.children():
			if isinstance(item,type):
				yield item
			else:
				if item.is_leaf():
					pass
				else:
					for thing in item.list_nodes(type):
						yield thing

	def immediate_text(self,should_strip=True,as_list=False):
		result = []
		for child in self.children():
			if isinstance(child,hiertext.TextLeaf):
				s = child.as_text()
				if should_strip:
					s = s.strip()
				if len(s):
					result.append(s)
		if as_list:
			return result
		else:
			return "\n".join(result)

class Root(_node):
	@staticmethod
	def is_root():
		return True

def belongs_with(*args):
	class a_class(_node):
		@staticmethod
		def can_be_within(other):
			if other in args:
				return True
			else:
				return super(a_class,self).can_be_within(other)
		@staticmethod
		def those_can_be_within():
			return copy.deepcopy(args)
	return a_class
	
class Nestable(_node):
	def should_clear(self):
		return False

def successive_possible_containers(a_node):
	return bfs.bfs(a_node,lambda x: x.those_can_be_within())
			
def closest_common_ancestor(x,y):
	x_list = list(	successive_possible_containers(x))
	y_list = list(	successive_possible_containers(y))
	X = set(x_list)
	Y = set(y_list)
	W = X.intersection(Y)
	enumerated_x_list = enumerate(x_list)
	chosen = [index for index,element in enumerated_x_list if element in W]
	return x_list[min(chosen)]

def path_to_descendant(x,y):
	inverse = invert_options_func.invert_options_func(y,lambda x: x.those_can_be_within())
	result = shortest_path.shortest_path(x,y,inverse)
	return result

if __name__ == "__main__":
	class html_entity(object):
		@classmethod
		def begin(cls,*args):
			return "<"+cls.__name__+">" 
		@classmethod
		def end(cls,*args):
			return "</"+cls.__name__+">" 
	class HTML(html_entity,Root): pass
	class BODY(html_entity,belongs_with(HTML)): pass
	class HEAD(html_entity,belongs_with(HTML)): pass
	class DIV(html_entity,belongs_with(BODY)): pass
	class SPAN(html_entity,belongs_with(DIV)): pass
	class P(html_entity,belongs_with(DIV,BODY)): pass
	class TITLE(html_entity,belongs_with(HEAD)): pass

	if 0:
		print path_to_descendant(HTML,P)
	else:
		def title(arg):
			return arg.title()
		import pytlml
		p = pytlml.PyTLML()
		print "doing main"
		p.main("START_HERE",globals())
		print "done main"
		print "outputting document as text"
		print p.root.as_text(True)
		print "done outputting document as text"


"""
START_HERE
\HTML
\TITLE
\title{A title}
\BODY
\DIV
\SPAN
\\ \\ \\ \\ \\
\\TEST TEST2
\end{SPAN}
\P

"""
