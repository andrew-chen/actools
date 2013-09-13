import acsetup
import acedu
from acedu.paths import position
from declare import test_for
from datetime import datetime
from resources import resource
from csv import DictReader
import fsitem

if False:
	"an example format of what a class_meeting_days argument should be"
	class_meeting_days = {
			"CSIS 221":[1,3]
			,
			"CSIS 221L":[2]
			,
			"CSIS 485":[2]
			,
			"CSIS 104":[1,2,3,4,5]
		,
		"CSIS 497":[]
	}
	todo = """

		Consider having this also generate an iCal file for Jamie and I to subscribe to....
	
		Generate the lesson plan files in the reverse order so that their access within TextWrangler will be more appropriate for my needs.

	"""


def mklp(class_meeting_days):
	"make lesson plans"
	p = position()
	course_test = test_for.course
	semester_test = test_for.semester
	if course_test(p):
		print "A Single Course"
		courses = [p]
		year = p.year
	elif semester_test(p):
		print (p.year,p.semester)
		year = p.year
		courses = p.courses()
	else:
		import sys
		print "error, neither in course nor semester directory"
		sys.exit(1)
	


	classes = {}


	for course in courses:
		name = course.basename()
		print name
		classes[name] = course
		meeting_days = class_meeting_days[name]
		classes[name].meeting_days = meeting_days
		lesson_plan_dir = course.lesson_plans()
		with open(resource("calendar_data.csv").item.path,"Urb") as cal_file:
			cal_data = DictReader(cal_file)
			for day in cal_data:
				if int(day["Class"]):
					date_string = day["Day"]+", "+day["Month"]+" "+day["Date"]+", "+str(year)
					date = datetime.strptime(date_string,"%A, %B %d, %Y")
					date = date.date()
					if date.isoweekday() in meeting_days:
						f = lesson_plan_dir.create(fsitem.File,str(date)+".txt")
						f.write(name+": "+course.semester+" "+str(year)+"""
""" + date.strftime("Lesson Plan for %A, %B "+str(date.day)+", "+str(year)+"""

"""))
