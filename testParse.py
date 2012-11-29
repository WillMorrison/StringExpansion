import sys
import Tokenize
import Parse

if (len(sys.argv) > 1):
	lines, expansionmap = Parse.Parse(Tokenize.Tokenize(sys.argv[1]))
	if (lines is not None):
		for line in lines:
			print ','.join(line)
		print "expansionmap is", expansionmap
else:
	print >> sys.stderr, "Error: An argument is required"

