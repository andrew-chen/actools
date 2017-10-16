import paginate

left="left"
right="right"
center="center"
auto="auto"
class Footer(object):
	def __init__(self,fstring,width=65,position=auto):
		self.format_string = fstring
		self.width = width
		self.position = position
		super(Footer,self).__init__()
	def _align(self,s,k):
		w = len(s)
		left = (self.width - w)/k
		result = " "*left+s
		return result
	def left(self,s):
		return self._align(s,self.width)
	def right(self,s):
		return self._align(s,1)
	def center(self,s):
		return self._align(s,2)
	def __call__(self,page_num):
		if self.position == center:
			return self.center(self.format_string.format(page_num))
		elif self.position == left:
			return self.left(self.format_string.format(page_num))
		elif self.position == right:
			return self.right(self.format_string.format(page_num))
		elif self.position == auto:
			if page_num%2:
				# odd, print on right
				return self.right(self.format_string.format(page_num))
			else:
				# even, print on left
				return self.left(self.format_string.format(page_num))
		else:
			raise ValueError, ".position attribute of instance of Footer class had invalid value"



if __name__ == "__main__":
	p = paginate.Paginator(footer_func=Footer("{0}"))
	p.add_line("hi")
	p.new_page()
	p.add_line("how are you?")
	p.new_page()
	p.add_line("bye")
	print p.document_as_text()
