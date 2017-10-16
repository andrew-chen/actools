"""
	A class that paginates
"""
class Paginator(object):
	def __init__(self,lines_per_page=49,footer_func=lambda x: ""):
		super(Paginator,self).__init__()
		self.pages = []
		self.lines_to_be_paginated = []
		self.lines_per_page = lines_per_page
		self.footer = footer_func
	def add_line(self,line):
		if len(self.lines_to_be_paginated) < self.lines_per_page:
			self.lines_to_be_paginated.append(line)
		self._normalize()
	def new_page(self):
		self.pages.append(self.lines_to_be_paginated)
		self.lines_to_be_paginated = []
	def clear_page(self):
		if len(self.lines_to_be_paginated):
			self.new_page()
		else:
			pass
	def _normalize(self):
		if len(self.lines_to_be_paginated) == self.lines_per_page:
			self.new_page()
	def _finalize(self):
		self.clear_page()
	def add_lines(self,lines,keep=True):
		if not keep:
			for line in lines:
				self.add_line(line)
		else:
			if len(lines) + len(self.lines_to_be_paginated) < self.lines_per_page:
				pass
			else:
				self.new_page()
			self.lines_to_be_paginated.extend(lines)
	def pages_as_text(self):
		self._finalize()
		for n,page in enumerate(self.pages,start=1):
			num_lines = len(page)
			page_text = ("\n".join(page))
			lines_to_add = (self.lines_per_page - num_lines)
			if lines_to_add > 3:
				for i in range(lines_to_add-3):
					page_text+="\n"
			if page_text[-2] != "\n": page_text+="\n"
			if page_text[-2] != "\n": page_text+="\n"
			page_text += self.footer(n)
			yield page_text
	def document_as_text(self):
		return chr(12).join(self.pages_as_text())

if __name__ == "__main__":
	p = Paginator()
	p.add_line("hi")
	p.add_lines(["how are you?","I am fine."])
	p.new_page()
	p.add_lines(["fancy meeting you here","come here often"])
	p._normalize()
	p._finalize()
	print list(p.pages_as_text())
	print p.document_as_text()
