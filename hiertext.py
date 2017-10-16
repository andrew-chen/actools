import hierbase
import declare

class TextContainer(hierbase.Container,declare.initializer(kind=object,meta=dict)):
	def addText(self,text):
		self.append(TextLeaf.from_str(text))
	def newChildContainer(self,kind):
		r = TextContainer()
		r.kind = kind
		self.append(r)
		return r
	def addChildContainer(self,value):
		self.append(value)
	def as_text(self,with_begin_end=False):
		result = ""
		if with_begin_end: result += self.begin()
		for child in self.children():
			result += child.as_text(with_begin_end)
		if with_begin_end: result += self.end()
		return result
class TextLeaf(hierbase.Leaf,declare.initializer(text=str,meta=dict)):
	@classmethod
	def from_str(cls,s):
		o = cls()
		o.text = s
		return o
	def as_text(self,with_begin_end=False):
		return self.text
