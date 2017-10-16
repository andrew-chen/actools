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

		Consider also factoring out the template for the generated file into a resource

	"""


def mklp(class_meeting_days,template=None,extension="txt"):
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
	

	default_template = """name+": "+course.semester+" "+str(year)+
 + date.strftime("Lesson Plan for %A, %B "+str(date.day)+", "+str(year))
	"""
	default_template = """{name}: {semester} {year}
Lesson Plan for {dayOfWeek}, {month} {day}, {year}
"""
	if template is None:
		template = default_template

	classes = {}


	for course in courses:
		name = course.basename()
		print name
		classes[name] = course
		meeting_days = class_meeting_days[name]
		classes[name].meeting_days = meeting_days
		try:
			lesson_plan_dir = course.lesson_plans()
		except IndexError:
			lesson_plan_dir = course.create(fsitem.Folder,"Lesson Plans")
		with open(resource("calendar_data.csv").item.path,"Urb") as cal_file:
			cal_data = list(reversed(list(DictReader(cal_file))))
			for day in cal_data:
				#print(day)
				if len(day["Class"]) and int(day["Class"]):
					date_string = day["Day"]+", "+day["Month"]+" "+day["Date"]+", "+str(year)
					date = datetime.strptime(date_string,"%A, %B %d, %Y")
					date = date.date()
					if date.isoweekday() in meeting_days:
						template_data = {"name":name,"semester":course.semester,"year":year,"dayOfWeek":date.strftime("%A"),"month":date.strftime("%B"),"day":date.day}
						print(template_data)
						formatted_data = template.format(**template_data)
						print(formatted_data)
						f = lesson_plan_dir.create(fsitem.File,str(date)+"."+extension)
						f.write(formatted_data)
