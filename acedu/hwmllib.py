import codecs
import locale
import sys

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 




import acsetup
import acedu.paths
from acedu.paths import meta

from fsitem import File

from acminidom import getText, attributesOf, parse

import os

import pprint

from hwml import Problem, Assignment

from collections import defaultdict

import string

class HWML_processor(object):

	def __init__(self):
		self.prepared = False

	def prepare_for_processing(self,verbose=True,path_sequence=None,ignore_chapter=False):
	
		if self.prepared:
			return self.code_list

		if path_sequence is None:
			self.d = acedu.paths.corresponding()
		else:
			self.d = path_sequence

		# I need a pretty printer for debugging purposes
		self.p = pprint.PrettyPrinter(indent=2)

		self.homeworks = []

		for homework_file in self.d:
			if verbose:
				print "parsing "+homework_file.path
			try:
				if homework_file.basename() != ".DS_Store":
					self.homeworks.append(parse(homework_file.path))
			except:
				print "parsing error in "+homework_file.path
				raise

		self.assignments = []

		for homework in self.homeworks:
			homework_assignments = homework.getElementsByTagName("assignment")
			if 0 == len(homework_assignments):
				print "Warning, encountered homework that had no assignment."
				print "outputing assignment"
				print homework.toprettyxml()
				sys.exit("Warning, encountered homework that had no assignment.")
			for assignment in homework_assignments:
				self.assignments.append(assignment)

		for assignment in self.assignments:
			attrs = attributesOf(assignment)
			try:
				assert(attrs["student"])
				print (attrs["student"])
				assert(attrs["book_edition"])
				assert(attrs["chapter"])
				problems = assignment.getElementsByTagName("problem")
				for problem in problems:
					attrs = attributesOf(problem)
					assert(attrs["number"])
					if verbose: print getText(problem.childNodes)
			except:
				print ("failed on "+str(attrs))
				raise

		self.assignments = map(Assignment,self.assignments)

		self.book_editions = defaultdict(list)
		for assignment in self.assignments:
			self.book_editions[assignment.book_edition].append(assignment)
		#print self.book_editions

		for assignment in self.assignments:
			if(ignore_chapter):
				pass
			elif(assignment.chapter != int(sys.argv[1])):
				print assignment.student
				assert(assignment.chapter == int(sys.argv[1]))
			num_probs = len(assignment.problems)
			if verbose: print "num_probs was "+str(num_probs)+" for student "+assignment.student

		self.problems = []

		for assignment in self.assignments:
			for problem in assignment.problems:
				prob_id = (assignment.book_edition,assignment.chapter,problem.number)
				prob_data = (assignment.student,problem.text)
				prob = (prob_id,prob_data)
				self.problems.append(prob)

		if verbose: print len(self.problems)
		
		self.problem_groups = defaultdict(list)

		self.code_list = []
		for problem in self.problems:
			prob_id, prob_data = problem
			assignment_student,problem_text = prob_data
			prob_code_data = (assignment_student,prob_id)
			prob_code = str(hash(prob_code_data))
			self.code_list.append((prob_code,prob_code_data))
			self.problem_groups[prob_id].append(prob_code+"\n"+("="*50)+"\n"+problem_text)

		if verbose: self.p.pprint(self.code_list)

		#print "by groups"
		self.count_by_groups = 0
		for group in self.problem_groups.values():
			self.count_by_groups += len(group)
		if verbose: print self.count_by_groups
		
		self.prepared = True
		
		return self.code_list
		
	def process_hwml(self,verbose=True):
		self.prepare_for_processing(verbose)

		another_count_by_groups = 0

		result = {"value":""}

		def output(value):
			if verbose:
				print value
			result["value"] = result["value"] + value.encode("ascii","ignore") + "\n"

		for key,value in self.problem_groups.items():
			book_edition,chapter,problem_number = key
			output( "In book edition "+str(book_edition)+" on problem "+str(problem_number) )

			for item in value:
				output( "="*50 )
				output( item )
				output( "="*50 )
				another_count_by_groups += 1
				output( "problem count is now: "+str(another_count_by_groups) )
				
		return result["value"]
			
	def detect_cheating(self,verbose=True):
		self.prepare_for_processing(verbose)
		
		problem_text_students = defaultdict(list)
		
		for assignment in self.assignments:
			for problem in assignment.problems:
				p_text = string.join(string.split(problem.text))
				problem_text_students[p_text].append(assignment.student)

		results = []

		for t,s in problem_text_students.items():
			if len(s) > 1:
				if verbose: print (t,s)
				results.append((t,s))

		return results

def process_problem_scores(code_list,the_file = False):
	problems = []

	if the_file:
		pass
	else:
		the_file = meta().file_with_name("problem_scores.csv").open("w")

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
		problem_groups[prob_id].append( problem( assignment_student, book_edition, chapter, problem_number, prob_code ) )
	
	another_count_by_groups = 0

	header = "Answer ID Number, Book Edition, Student Name, Problem Number, Problem Order, Score, Notes"
	if the_file:
		the_file.write(header+"\n")
	else:
		print header

	for key,value in problem_groups.items():
		book_edition,chapter,problem_number = key
		for item in value:
			another_count_by_groups += 1
			to_write = str(item.code)+", "+str(book_edition)+", "+str(item.student)+", "+str(item.number)+", "+str(another_count_by_groups)
			if the_file:
				the_file.write(to_write+"\n")
			else:
				print to_write
		
		
def process_hwml():
	hp = HWML_processor()
	return hp.process_hwml()

def detect_cheating():
	hp = HWML_processor()
	return hp.detect_cheating()

def detect_cheating_on_these(list_of_paths):
	hp = HWML_processor()
	print "passing in list_of_paths that are "+str(list_of_paths)
	hp.prepare_for_processing(path_sequence=(map(File,list_of_paths)),ignore_chapter=True)
	hp.detect_cheating()
	