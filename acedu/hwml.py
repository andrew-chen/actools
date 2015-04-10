from acminidom import getText, attributesOf

class Problem(object):
	def __init__(self,theNode):
		attrs = attributesOf(theNode)
		self.number = int(attrs["number"])
		self.text = getText(theNode.childNodes)

class Assignment(object):
	def __init__(self,theNode):
		attrs = attributesOf(theNode)
		self.student = attrs["student"].strip()
		self.book_edition = int(attrs["book_edition"])
		self.chapter = int(attrs["chapter"])
		try:
			self.problems = [Problem(problem) for problem in theNode.getElementsByTagName("problem")]
		except:
			print "error in processing problems for assignment "+str((self.chapter,self.student))
			raise


