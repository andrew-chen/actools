import codecs
import locale
import sys

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 




import acsetup
import acedu.paths
from fsitem import File

from acminidom import getText, attributesOf, parse

import os

import pprint

from hwml import Problem, Assignment

from collections import defaultdict

import string

class HWML_processor(object):

	def prepare_for_processing(self):

		self.d = acedu.paths.corresponding()

		# I need a pretty printer for debugging purposes
		self.p = pprint.PrettyPrinter(indent=2)

		self.homeworks = []

		for homework_file in self.d:
			try:
				if homework_file.basename() != ".DS_Store":
					self.homeworks.append(parse(homework_file.path))
			except:
				print "parsing error in "+homework_file.path
				raise

		self.assignments = []

		for homework in self.homeworks:
			for assignment in homework.getElementsByTagName("assignment"):
				self.assignments.append(assignment)

		if True:
			for assignment in self.assignments:
				attrs = attributesOf(assignment)
				print attrs["student"]
				print attrs["book_edition"]
				print attrs["chapter"]
				problems = assignment.getElementsByTagName("problem")
				for problem in problems:
					attrs = attributesOf(problem)
					print attrs["number"]
					print getText(problem.childNodes)

		self.assignments = map(Assignment,self.assignments)

		self.book_editions = defaultdict(list)
		for assignment in self.assignments:
			self.book_editions[assignment.book_edition].append(assignment)
		#print self.book_editions

		for assignment in self.assignments:
			assert(assignment.chapter == int(sys.argv[1]))
			num_probs = len(assignment.problems)
			print "num_probs was "+str(num_probs)+" for student "+assignment.student

		self.problems = []

		for assignment in self.assignments:
			for problem in assignment.problems:
				prob_id = (assignment.book_edition,assignment.chapter,problem.number)
				prob_data = (assignment.student,problem.text)
				prob = (prob_id,prob_data)
				self.problems.append(prob)

		print len(self.problems)
		
		self.problem_groups = defaultdict(list)

		self.code_list = []
		for problem in self.problems:
			prob_id, prob_data = problem
			assignment_student,problem_text = prob_data
			prob_code_data = (assignment_student,prob_id)
			prob_code = str(hash(prob_code_data))
			self.code_list.append((prob_code,prob_code_data))
			self.problem_groups[prob_id].append(prob_code+"\n"+("="*50)+"\n"+problem_text)

		self.p.pprint(self.code_list)

		#print "by groups"
		self.count_by_groups = 0
		for group in self.problem_groups.values():
			self.count_by_groups += len(group)
		print self.count_by_groups
		
	def process_hwml(self):
		self.prepare_for_processing()

		another_count_by_groups = 0

		for key,value in self.problem_groups.items():
			book_edition,chapter,problem_number = key
			print "In book edition "+str(book_edition)+" on problem "+problem_number

			for item in value:
				print "="*50
				print item
				print "="*50
				another_count_by_groups += 1
				print "problem count is now: "+str(another_count_by_groups)
			
	def detect_cheating(self):
		self.prepare_for_processing()
		
		problem_text_students = defaultdict(list)
		
		for assignment in self.assignments:
			for problem in assignment.problems:
				p_text = string.join(string.split(problem.text))
				problem_text_students[p_text].append(assignment.student)

		for t,s in problem_text_students.items():
			if len(s) > 1:
				print (t,s)

def process_problem_scores(code_list):
	problems = []

	class problem(object):
		def __init__(self,student,book_edition,chapter,number,code):
			self.student = student
			self.book_edition = book_edition
			self.chapter = chapter
			self.number = number
			self.code = code

	from collections import defaultdict

	problem_groups = defaultdict(list)

	for code_item in code_list:
		(prob_code,prob_code_data) = code_item
		(assignment_student,prob_id) = prob_code_data
		(book_edition,chapter,problem_number) = prob_id
		problem_groups[prob_id].append(problem(assignment_student,book_edition,chapter,problem_number,prob_code))
	
	another_count_by_groups = 0

	print "Answer ID Number, Book Edition, Student Name, Problem Number, Problem Order, Score, Notes"

	for key,value in problem_groups.items():
		book_edition,chapter,problem_number = key
		for item in value:
			another_count_by_groups += 1
			print str(item.code)+", "+str(book_edition)+", "+str(item.student)+", "+str(item.number)+", "+str(another_count_by_groups)
		
		
def process_hwml():
	hp = HWML_processor()
	hp.process_hwml()

def detect_cheating():
	hp = HWML_processor()
	hp.detect_cheating()
