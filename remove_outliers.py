from itr import itr
def remove_outliers(src,k=1):
	"""
		src is a iterable,
		and the result of this will be an iterable

		we will remove anything that is further away from everything else than anything else is from each other
		we are assuming numeric values and nothing else

		should rewrite this to use the stats module,
		and should identify outliers as those whose distance from the mean and from their nearest neighbors is greater than 2*mean
		or something like that
	"""
	deltas = []
	#print "deltas is "+str(deltas)
	for p,c,n in itr(sorted(list(src))).pcn_iter():
		if p is None: pass
		else: deltas.append(c-p)
	#print "deltas is "+str(deltas)
	deltas = list(set(deltas))
	#print "deltas is "+str(deltas)
	deltas = deltas[:-(k)] # exclude the last k
	#print "deltas is "+str(deltas)
	for p,c,n in itr(sorted(list(src))).pcn_iter():
		if p is None:
			#print "yielding "+str(c)
			yield c
		else: 
			if (c-p) in deltas:
				#print "yielding "+str(c)
				yield c
			else:
				#print str(c)+"-"+str(p)+" was not in deltas"
				pass
