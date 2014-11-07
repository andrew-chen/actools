from acminidom import getText, attributesOf

class Problem(object):
	def __init__(self,theNode):
		attrs = attributesOf(theNode)
		self.number = int(attrs["number"])
		self.text = getText(theNode.childNodes)

class Assignment(object):
	def __init__(self,theNode):
		attrs = attributesOf(theNode)
		self.student = attrs["student"]
		self.book_edition = int(attrs["book_edition"])
		self.chapter = int(attrs["chapter"])
		self.problems = [Problem(problem) for problem in theNode.getElementsByTagName("problem")]


