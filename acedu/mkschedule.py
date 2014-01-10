import os
import os.path
from acedu.paths import position
from declare import test_for
import sys
from actypes import dummy_object

"""
	Reads the lesson plan files,
	and assumes the have the following format:

	class info line
	lesson plan info line
	blank line
	summary lines
	other stuff

	with filename of YYYY-MM-DD.txt

	and extracts out the date and summary line
	and generates an appropriate (HTML or LaTeX or both)
	file for that class,

	(the following won't be done just yet)
	and eventually generates a file that I can click to
	open in the editor and watches and auto-refreshes
"""

class LessonPlanFile(object):
	def __init__(self,path_to_file):
		filename = os.path.basename(path_to_file)
		filename,ext = os.path.splitext(filename)
		assert(ext == ".txt")
		(Y,M,D) = tuple(map(lambda x: int(x.lstrip("0")),filename.split("-")))
		with open(path_to_file,"Ur") as the_lesson_plan:
			line1 = the_lesson_plan.readline()
			line2 = the_lesson_plan.readline()
			line3 = the_lesson_plan.readline()
			assert(len(line3.strip()) == 0)
			summary = []
			current_line = the_lesson_plan.readline().strip()
			while len(current_line):
				summary.append(current_line)
				current_line = the_lesson_plan.readline().strip()
			self.summary = summary
			self.year = Y
			self.month = M
			self.day = D
			self.class_header = line1
			self.day_header = line2
			other_stuff = []
			for line in the_lesson_plan.readlines():
				other_stuff.append(line)
			self.other_stuff = other_stuff
	def print_text_line(self):
		print str(self.month)+", "+str(self.day)+", "+str(self.summary)
	def print_with_template_engine(self,template_engine ):
		template_engine(self.month,self.day,self.summary)
		

def process_list_of_lesson_plan_file_full_paths(args,template_engine = 0):
	if template_engine == 0:
		def print_the_arg(arg):
			print arg
		def print_three_args(arg1,arg2,arg3):
			print str(arg1)+", "+str(arg2)+", "+str(arg3)
		template_engine = dummy_object()
		template_engine.print_header = print_the_arg
		template_engine.lesson_plan_printer = print_three_args
	files = sorted(args)
	lesson_plans = map(LessonPlanFile,files)
	template_engine.print_header(lesson_plans[0].class_header)
	# eventually use itr and group_while to get months together and such
	for lesson_plan in lesson_plans:
		lesson_plan.print_with_template_engine(template_engine.lesson_plan_printer)

def process_lesson_plans_for_course(the_year,the_semester,the_course,template_engine = 0):
	path = "/Users/chenan/Documents/Courses/"
	path = path + str(the_year) + "/" + the_semester + " " + str(the_year)
	path = path + "/" + the_course + "/Lesson Plans"
	filenames = os.listdir(path)
	lesson_plan_filenames = []
	for filename in filenames:
		if filename != ".DS_Store":
			lesson_plan_filenames.append(os.path.join(path,filename))
	process_list_of_lesson_plan_file_full_paths(lesson_plan_filenames,template_engine)

def process_lesson_plans_for_current_courses(template_engine = 0):
	p = position()
	course_test = test_for.course
	semester_test = test_for.semester
	if course_test(p):
		if not template_engine: print "A Single Course"
		courses = [p]
		year = p.year
	elif semester_test(p):
		if not template_engine: print (p.year,p.semester)
		year = p.year
		courses = p.courses()
	else:
		print "error, neither in course nor semester directory"
		sys.exit(1)

	classes = {}

	for course in courses:
		name = course.basename()
		#print name
		classes[name] = course
		process_lesson_plans_for_course(course.year,course.semester,name,template_engine)

if __name__ == "__main__":
	process_lesson_plans_for_course(2013,"Spring","CSIS 320")
	process_lesson_plans_for_course(2013,"Spring","CSIS 190")
	process_lesson_plans_for_course(2013,"Spring","GDEV 190")
