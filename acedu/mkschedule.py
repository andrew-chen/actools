import os
import os.path
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

def process_list_of_lesson_plan_file_full_paths(args):
	files = sorted(args)
	lesson_plans = map(LessonPlanFile,files)
	print lesson_plans[0].class_header
	# eventually use itr and group_while to get months together and such
	for lesson_plan in lesson_plans:
		lesson_plan.print_text_line()

def process_lesson_plans_for_course(the_year,the_semester,the_course):
	path = "/Users/chenan/Documents/Courses/"
	path = path + str(the_year) + "/" + the_semester + " " + str(the_year)
	path = path + "/" + the_course + "/Lesson Plans"
	filenames = os.listdir(path)
	lesson_plan_filenames = []
	for filename in filenames:
		if filename != ".DS_Store":
			lesson_plan_filenames.append(os.path.join(path,filename))
	process_list_of_lesson_plan_file_full_paths(lesson_plan_filenames)

if __name__ == "__main__":
	process_lesson_plans_for_course(2013,"Spring","CSIS 320")
	process_lesson_plans_for_course(2013,"Spring","CSIS 190")
	process_lesson_plans_for_course(2013,"Spring","GDEV 190")
