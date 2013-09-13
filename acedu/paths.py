import acsetup
import fsitem
from decorator import Decorator

def courses():
	h = fsitem.home()
	return h["Documents"]["Courses"]

def year(yr):
	class _Year(Decorator):
		def is_year(self):
			return True
		def semester(self,name):
			s = str(name)+" "+str(yr)
			s = _Semester(self.__getitem__(s))
			s.year = yr
			s.semester = name
			return s
	return _Year(courses()[str(yr)])

class _Course(Decorator):
	def is_course(self):
		return True
	def data(self):
		return self.__getitem__("Data")
	def code(self):
		return self.__getitem__("Code")
	def lesson_plans(self):
		return self.__getitem__("Lesson Plans")

class _Semester(Decorator):
	def is_semester(self):
		return True
	def course(self,name):
		c = _Course(self.__getitem__(name))
		c.semester = self.semester
		c.year = self.year
		c.course = name
		return c
	def courses(self):
		return [self.course(item.basename()) for item in self.folders() if 2 == len(item.basename().split())]
		

def position(where=None):
	if where is None:
		ancestors = list(fsitem.current().ancestors())
	else:
		ancestors = list(where.ancestors())
	c = courses()
	c_a = [item.path for item in c.ancestors()]
	l = [item for item in ancestors if item.path not in c_a and item.path != c.path]
	if len(l) > 0:
		p = l[-1]
		yr = int(p.basename())
		yr = year(yr)
	if len(l) > 1:
		p = l[-2]
		full_semester = p.basename()
		semester,space,ear = full_semester.partition(" ")
		sem = yr.semester(semester)
	if len(l) > 2:
		p = l[-3]
		course = sem.course(p.basename())
		return course
	if len(l) > 1:
		return sem
	if len(l) > 0:
		return yr

def corresponding(where=None):
	if where is None:
		where = fsitem.current()
	p = position()
	d = p.data()
	s = where - p.code()
	return d[s]


if __name__ == "__main__":
	print position().__dict__.values()[0].__dict__
