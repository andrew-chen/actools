import acsetup
from fsitem import Folder
global resource_folders
resource_folders = [i for d in map(Folder,acsetup.data_paths) for i in d.items()  if i.basename() == "Resources"]

# should make something similar for object persistence

class resource(object):
	def __init__(self,name):
		global resource_folders
		for f in resource_folders:
			for item in f.items():
				basename = item.basename()
				if basename == name:
					self.item = item
					return
		raise ValueError, "Not a resource name"
	def data(self):
		return self.item.read()
	def lines(self):
		return self.item.readlines()
	def Lines(self):
		return self.item.read_Lines()

if __name__ == "__main__":
	print map(lambda x: x.path,resource_folders)
