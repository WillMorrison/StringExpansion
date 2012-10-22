import sys
import Parse

if (len(sys.argv) > 1):
	lines = Parse.Parse(Tokenize(sys.argv[1]))
	if (lines is not None):
		for line in lines:
			print ','.join(line)
else:
	print >> sys.stderr, "Error: An argument is required"

