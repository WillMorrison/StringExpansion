import itertools

################################################################################
# Generates a series of formatted numerical strings. Formatting consists of
# generating leading zeroes based on the two input strings.
################################################################################
def NumRange( first, last, step=1):
	# calculate the number of common leading zeroes
	prefixzeroes = min(len(list(itertools.takewhile(lambda x: x == '0', first))), 
	                   len(list(itertools.takewhile(lambda x: x == '0', last))))
	
	# calculate the length to zero pad to
	padwidth = min(len(first), len(last)) - prefixzeroes

	# build a range and return formatted values from it
	for num in xrange(int(first), int(last)+1, int(step)):
		yield '0'*prefixzeroes + '{:0{width}}'.format(num,width=padwidth)
