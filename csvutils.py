def trim_keys(a_dict):
	"""
		In case keys in a dictionary have extra white space on either side,
		this can be used to trim that.
		
		Not uncommon for hand-crafted CSV files,
		since humans will often want to put in the spaces for readability
	"""
	keys = a_dict.keys()
	new_dict = {}
	for key in keys:
		if len(key) == 0 and len(a_dict[key]) == 0:
			pass
		else:
			new_dict[key.strip().strip("\xef\xbb\xbf")] = a_dict[key]
	return new_dict

import acsetup
import actypes
import csv
import fsitem

def read_csv_file(the_file,**kwargs):
	da = actypes.DictAdaptor(**kwargs)
	with fsitem.safe_open(the_file,"Ur") as the_open_file:
		the_reader = csv.DictReader(the_open_file)
		try:
			for item in the_reader:
				try:
					trimmed = trim_keys(item)
				except:
					print(the_file)
					raise
				try:
					yield da.from_dict(trimmed)
				except KeyError:
					pass
		except:
			print(the_file)
			raise

def write_csv_file(the_file,list_of_items,key_ordering=lambda x:sorted(x),**kwargs):
	"""
		go through list_of_items and see if any have the _dict_adaptor_info attribute,
		and aggregate that from all of them to get a default list of what to write out,
		and use that if kwargs is empty, otherwase use kwargs.
		
		for determining the order in which to write things out, pass the column headers through key_ordering
		and use that to construct the list
		
		then use csv.DictWriter to write it all out
		
		WORK HERE
	"""
	pass
