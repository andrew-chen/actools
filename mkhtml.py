import acsetup
from creating import AttributeFactory
class Tag(object):
	def __init__(self,name):
		self.name = name
		self.attributes = {}
		self.children = list()
	def __call__(self,*args,**kwargs):
		r = Tag(self.name)
		r.children.extend(args)
		r.attributes.update(kwargs)
		return r
	def __str__(self,indentation_level=0):
		indentation = " "*indentation_level
		attrs = ""
		attrs = " ".join([str(key)+'="'+str(value)+'"' for (key,value) in self.attributes.items()])
		if len(attrs):
			attrs = " "+attrs
		open_tag = "<"+self.name+attrs+">\n"
		children_str = []
		for child in self.children:
			try:
				children_str.append(child.__str__(indentation_level+1))
			except TypeError:
				children_str.append(indentation+" "+str(child)) # when the child is not a Tag object
		close_tag = "</"+self.name+">\n"
		# put it all together
		result = indentation+open_tag+"".join(children_str)+indentation+close_tag
		return result

		

tag = AttributeFactory(Tag)

html = tag.html
body = tag.body
a = tag.a
ul = tag.ul
ol = tag.ol
li = tag.li
p = tag. p
code = tag.code
pre = tag.pre
if __name__ == "__main__":
	print(html(body(a("here",href="."),ul(li("hi"),li("bye")),a("there",href=".."))))

