import sys
import Tokenize
import Parse
import itertools

if (len(sys.argv) > 1):
	lines, expansionmap = Parse.Parse(Tokenize.Tokenize(sys.argv[1]))
	if (lines is not None):
		for sentence in itertools.product(*lines):
			print ''.join(map (lambda i: sentence[i-1], expansionmap) )
else:
	print >> sys.stderr, "Error: An argument is required"

