"""
	Question List processor - support

	Processes question list files

	Can be made more modular.
"""
import acsetup
import acedu.paths
import sys
from collections import defaultdict
import remove_outliers

class QuestionList(object):
	def __init__(self,maxCount):
		self.y = []  # yes
		self.n = []  # no
		self.b = []  # both
		self.yp = [] # extra yes problems
		self.np = [] # extra no problems
		self.max_count = maxCount
	def addYes(self,num):
		if num in self.n:
			self.b.append(num)
			self.n.remove(num)
			return
		if num in self.np:
			self.b.append(num)
			self.np.remove(num)
			return
		if num in self.b or num in self.y or num in self.yp:
			return
		if len(self.y) <= self.max_count:
			self.y.append(num)
		else:
			print "had extra yes question of "+str(num)
			self.yp.append(num)
	def addNo(self,num):
		print "no of "+str(num)
		if num in self.y:
			self.b.append(num)
			self.y.remove(num)
			return
		if num in self.yp:
			self.b.append(num)
			self.yp.remove(num)
			return
		if num in self.b or num in self.n or num in self.np:
			return
		if len(self.n) <= self.max_count:
			self.n.append(num)
		else:
			print "had extra no question of "+str(num)
			self.np.append(num)

def leadingDigits(s):
	"takes a string and returns the substring that is the leading digits"
	result = []
	for c in s:
		if c.isdigit():
			result.append(c)
		else:
			break
	result = "".join(result)
	return result

class QuestionListReader(object):
	"used in reading in a question list"
	def __init__(self,maxCount,person):
		self.state = 0
		self.penaltyCount = 0
		self.result = QuestionList(maxCount)
		self.person = person
	def processString(self,s):
		ld = leadingDigits(s)
		if len(ld) > 0:
			self.addNumber(int(ld))
			#if ld != s:
			#	self.addPenalty("extraneous data after a number")
		elif s[0] == "y" or s[0] == "Y":
			self.state = "y"
			print "switching to yes based on: "+s
		elif s[0] == "n" or s[0] == "N":
			self.state = "n"
			print "switching to no based on: "+s
		else:
			print "encountered extra text of: "+s
	def addPenalty(self,reason):
		self.penaltyCount = self.penaltyCount + 1
		print "penalty for "+self.person+" "+reason
	def addNumber(self,num):
		if self.state == 0:
			self.addPenalty("not being in an appropriate state")
		elif self.state == "y":
			self.result.addYes(num)
		elif self.state == "n":
			self.result.addNo(num)
		else:
			self.badError("Shouldn't get here!")

def readFile(filename,maxCount):
	"returns a QuestionList"
	reader = QuestionListReader(maxCount,filename)
	lines = open(filename).readlines()
	for line in lines:
		sline = line.strip()
		if len(sline) > 0:
			reader.processString(sline)
	r = reader.result
	if len(r.b) > 0:
		reader.addPenalty("something in both")
	if len(r.yp) > 0:
		reader.addPenalty("too many yes")
	if len(r.np) > 0:
		reader.addPenalty("too many no")
	return (reader.penaltyCount,r.y,r.n,filename)


def processQuestions(
	assignment_name,
	NUMBER_EACH,
	NUMBER_CHOSEN,
	files = None,
	maxKey = None
):
	"""
		processes the questions
	"""

	if files == None:
		position = acedu.paths.position()
		assignment_dir = position.data()[assignment_name]
		assignment_files = [item for item in assignment_dir.files() if item.basename() != ".DS_Store"]
		results = { assignment_file.basename() : readFile(assignment_file.path,NUMBER_EACH) for assignment_file in assignment_files }
	else:
		results = { f.basename() : readFile(f.path,NUMBER_EACH) for f in files }
	print results


	yesCounts = {}
	noCounts = {}

	print "now outputting penalty count"
	for key in sorted(results.keys()):
		p,y,n,f = results[key]
		print str(p)+"	"+key
		yield (p,key,f)
		for yes in y:
			yesCounts[yes] = 1+yesCounts.get(yes,0)
		for no in n:
			noCounts[no] = 1+noCounts.get(no,0)


	print "now outputting yes counts by number"
	for key in sorted(yesCounts.keys()):
		print str(key)+"	"+str(yesCounts[key])

	print "now outputting yes counts by count"
	from collections import defaultdict
	count_dict_for_output = defaultdict(list)
	for key,value in sorted(yesCounts.items()):
		count_dict_for_output[value].append(key)
	for key,value in sorted(count_dict_for_output.items()):
		print str(key)+"	"+str(value)

	print "now outputting no counts"
	for key in sorted(noCounts.keys()):
		print str(key)+"	"+str(noCounts[key])

	keys = sorted(list(set(sorted(yesCounts.keys())).union(set(sorted(noCounts.keys())))))
	print keys
	if maxKey is None:
		maxKey = max(keys)
	
	print maxKey

	# now we compose tuples of the form (noCount,yesCount,key), put them in a list, sort it,
	# and then identify if there are ties at the border, and print out the NUMBER_CHOSEN plus ties
	# this way I can easily see what are likely to be the decisions that I need to make

	listResult = []
	for i in range(maxKey):
		key = i+1
		listResult.append((noCounts.get(key,0),-1*yesCounts.get(key,0),key),)
	thoseToChoose = sorted(listResult)
	count = 1
	lastYCount, lastNCount = 0,0
	print "now outputting those to choose (1)"
	reallyThoseToChoose = []
	wasTie = 0
	for item in thoseToChoose:
		print item
		n,y,p = item
		if count > NUMBER_CHOSEN:
			if n == lastNCount and y == lastYCount:
				reallyThoseToChoose.append((p,"tie"),)
				wasTie = 1
			else:
				break
		else:
			reallyThoseToChoose.append((p,""),)
		lastNCount, lastYCount = n,y
		count = count + 1
	print "now outputting those to choose (2)"
	if wasTie:
		print "there was a tie!"
		for item in sorted(reallyThoseToChoose):
			print item
	else:
		for item in sorted(reallyThoseToChoose):
			p,t = item
			print str(p)+", ",
	
