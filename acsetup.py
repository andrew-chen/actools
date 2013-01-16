import sys
from fsitem import current, Folder, File

# consider moving to /Library/Python/2.7/site-packages

data_paths = []

d = current()

p = d.parent()
while p.path is not d.path:
	for item in d.folders():
		b = item.basename()
		if b == "Data":
			data_paths.append(item.path)
		elif b == "Code":
			foundactools = 0
			for child in item.items():
				if isinstance(child,Folder):
					if child.basename() == "actools":
						foundactools = 1
						if child.path not in sys.path:
							sys.path.append(child.path)
						break
			if not foundactools:
				if item.path not in sys.path:
					sys.path.append(item.path)
	d = p
	p = d.parent()

if __name__ == "__main__":
	print "Code:"
	print sys.path
	print "Data:"
	print data_paths
