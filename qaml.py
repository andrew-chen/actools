import acsetup
from pypdtd import belongs_with, Root

class qml_entity(object):
	@classmethod
	def begin(cls,*args):
		return "<"+cls.__name__+">" 
	@classmethod
	def end(cls,*args):
		return "</"+cls.__name__+">" 
	
def comment(arg):
	return ""
#def ll(arg):
#	return "all of the above"
# no(arg):
#	return "none of the above"
class QML(qml_entity,Root): pass
class BODY(qml_entity,belongs_with(QML)): pass
class HEAD(qml_entity,belongs_with(QML)): pass
class TITLE(qml_entity,belongs_with(HEAD)): pass
class q(qml_entity,belongs_with(BODY)): pass
class a(qml_entity,belongs_with(q)): pass
class correct(qml_entity,belongs_with(q)): pass
class w(qml_entity,belongs_with(q)): pass
#class code(qml_entity,belongs_with(q)): pass
class code(qml_entity,belongs_with(q,a)): pass




if __name__ == "__main__":
	if 0:
		print path_to_descendant(HTML,P)
	else:
		import pytlml
		p = pytlml.PyTLML()
		print "doing main"
		p.main("START_HERE",globals())
		print "done main"
		print "outputting document as text"
		print p.root.as_text(True).strip()
		print "done outputting document as text"


"""
START_HERE
\QML
\TITLE
\title{A title}
\BODY
\q Question text
\a Answer 1
\a Answer 2
\\ \\ \\ \\ \\
\\TEST TEST2
\end{BODY}

"""
