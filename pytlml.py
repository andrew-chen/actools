import acsetup
"""
	Provides TeX-like syntax,
	could be useful in certain contexts later on

	Should factor out some code

	Should add support for not just the implicit closing,
	but also the implicit opening,
	if there are relations between classes.
	Need some convention to indicate these relations,
	perhaps a class variable that indicates what the
	container class should be.
	Could even do implicit closing _and_ implicit opening,
	if the hierarchy of classes is exposed and navigable.

	Will likely want to capture the output for possible later processing,
	will need to integrate with other classes to achieve this.

	Or, could provide different ways of having output,
	but would need to figure out how to specify that separately.

	Key anticipated use case: for writing literate JavaScript programs,
	and then generating them from there,
	since JavaScript is such a mess and there's no good
	literate JS tool out there that I know of.
"""
import fsitem
import sys
import re
import escaping
import superstack
import pypdtd 
import hiertext

class PyTLML(object):
	def __init__(self):
		self.stack = superstack.CommonStack()
		self.root = None
	def list_nodes(self,type=pypdtd._node):
		for item in self.root.children():
			if isinstance(item,type):
				yield item
			else:
				if item.is_leaf():
					pass
				else:
					for thing in item.list_nodes(type=type):
						yield thing

	def main(self,arg=False,scope=globals(),filename=None):
		self.scope = scope
		if filename is None:
			lines = fsitem.fs_object(sys.argv[1]).read_Lines()
		else:
			try:
				lines = fsitem.fs_object(filename).read_Lines()
			except AttributeError:
				print("could not access "+filename)
				sys.exit(1)
		if arg:
			started = False
		else:
			started = True
		for line in lines:
			if started:
				self.handle_line(line)
				self.addText("\n")
			elif line.text.startswith(arg):
				started = True
		#print self.end_all()

	def addText(self,text):
		if len(text) == 0:
			return
		#sys.stdout.write(text)
		try:
			self.stack.top_value().addText(text)
		except:
			try:
				self.root.addText(text)
			except:
				print "warning, text was not added to the document. Text was: '"+text+"'"
	def showText(self,text):
		#sys.stdout.write(text)
		pass

	def handle_line(self,line):
		text = line.text[:-1] # strip off that last newline
		self.current_line = line
		self.handle_text(text)
	def handle_text(self,text):
		fragments = text.split("\\")
		if len(fragments) < 2:
			self.addText(text)
			return
		self.addText(fragments[0])
		remaining_fragments = fragments[1:]

		items_to_process = map(self.separate_command,remaining_fragments)
		def sentinel_test(arg):
			return (( arg[1] == None ) and ( 0 == len(arg[0]+arg[2]) ))
		def process_special(arg):
			return (None,None,'\\'+arg[0]+arg[2])
		for command,cmd_parts,plain in escaping.unescape(sentinel_test,items_to_process,process_special):
			self.handle_command(cmd_parts)
			self.addText(plain)

	def separate_command(self,text):
		"""
			\\	No command, just an escaped backslash
			\expr{...}	if expr is begin, then the ... is evaled and then called
					if expr is anything else, then if the ... has no spaces, then the ... is seen as a type name,
					and the stack is popped (if necessary) so that something with that type is on the top,
					and then expr is treated as a method name which is invoked on the top value
					if expr is not begin and if ... has whitespace in it, then expr is treated as a function name,
					and the ... is a string that is passed into it
			\expr{...}[...] like \expr{...} except [...] is passed in as an argument to that method name
			\expr	Implicitly the same as \begin{expr} but with the endings of any others that are on the stack

			expr is any sequence of characters that do not contain whitespace, (, or left curly brace
		"""
		m = re.match(r"(?P<method>[^\s{]*)(\{(?P<args>[^}]*)\}(\[(?P<params>[^]]*)\])?)?",text)
		method = m.group('method')
		args = m.group('args')
		params = m.group('params')
		rest = text[m.end(0):]
		command = text[:m.end(0)]
		assert(text == command+rest)
		if method:
			return (command,(method,args,params),rest)
		else:
			return (command,None,rest)


	def handle_command(self,command):
		if command is None: return ""
		method,args,params = command
		if args:
			self.handle_complex_command(command)
		else:
			v = eval(method,self.scope)
			try:
				vv = v()
			except TypeError:
				print "{number}, '{text}', {file.path}".format(**(self.current_line.__dict__))
				print "You did not pass in an argument to a command that takes an argument"
				raise
			self.begin(method,vv)

	def begin(self,func_name,value,clear=True,meta={}):
		result = ""
		if self.root == None:
			if value.is_root():
				self.root = value
			else:
				raise SyntaxError, "document did not have an outtermost root element"
		if not self.stack.empty():
			if self.stack.top_type() == func_name:
				if clear:
					result += self.stack.pop_value().end()
			else:
				anc = pypdtd.closest_common_ancestor(value.__class__,self.stack.top_value().__class__)
				self.showText(self.clear_until(anc.__name__))
				# would need to push any intermediates here....
				try:
					to_push = pypdtd.path_to_descendant(anc,value.__class__)
					to_push = to_push[1:-1] # we don't need what we already have on there, or what we're about to add
					for item in to_push:
						i = item()
						self.showText( i.begin() )
						self.stack.top_value().addChildContainer(i)
						self.stack.push(item.__name__,i)
				except ValueError:
					# presumably this is because we need to clear some stuff
					#print anc.__name__,value.__class__.__name__
					self.showText(self.clear_just_beyond(anc.__name__))					
				value.meta = meta
			self.stack.top_value().addChildContainer(value)
		self.stack.push(func_name,value)
		self.showText( value.begin() )

	def clear_just_beyond(self,type_name):
		result = ""
		for item in self.stack.pop_value_until_just_beyond_type(type_name).end():
			result += item
		return result

	def clear_until(self,type_name):
		result = ""
		for item in self.stack.pop_value_until_type(type_name).end():
			result += item
		return result

	def end(self,type_name,params):
		result = self.clear_until(type_name)
		result+= self.stack.pop_value().end(params)
		return result

	def method(self,type_name,method_name,params):
		result = self.clear_until(type_name)
		result += getattr(self.stack.top_value(),method_name)(params)
		return result

	def handle_complex_command(self,command):
		method,args,params = command
		stack = self.stack
		if method == "begin":
			o = eval(args,self.scope)(params)
			self.showText( self.begin(args,o,o.should_clear(),meta={"params":params}) )
		elif method == "end":
			self.showText( self.end(args,params) ) # params on end discouraged
		else:
			if len([char for char in args if char.isspace()]):
				try:
					to_eval = method+"("+repr(args)+")"
					self.handle_text(eval(to_eval,self.scope))
				except NameError:
					print "{number}, '{text}', {file.path}".format(**(self.current_line.__dict__))
					print "You attempted to call a command that does not exist"
					raise
				except TypeError:
					print "{number}, '{text}', {file.path}".format(**(self.current_line.__dict__))
					print "Unknown TypeError for trying to eval: "+str(to_eval)
					raise
			else:
				try:
					self.showText( self.method(args,method,params) ) # params on others discouraged, and others in general discouraged
				except IndexError:
					print "{number}, '{text}', {file.path}".format(**(self.current_line.__dict__))
					print "You did pass in an argument to a command that does not take an argument"
					raise
					
					
	def end_all(self):
		result = ""
		for item in self.stack.value_pop_all().end():
			result += item
		return result

class Item(object):
	def begin(self): return "<li>"
	def end(self): return "</li>"

class Test(object):
	def __init__(self): self.whatever = 1
	def begin(self): return "beginning test"
	def end(self): return "ending test"
	def other(self): return "other in test"

vertical_bar = "|"

if __name__ == "__main__":
	p = PyTLML()
	print "doing main"
	p.main("START_HERE")
	print "done main"
	print "outputting document as text"
	print p.root.as_text(True)
	print "done outputting document as text"

"""
START_HERE
\begin
\begin{Test}
\begin{Test}[params]
\begin{Item()}
\begin{Item()}
\begin{Item()}
\other{Test}
\begin{Item()}
\end{Test}
"""
