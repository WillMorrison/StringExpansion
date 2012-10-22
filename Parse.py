import itertools
import sys

################################################################################
# This takes an iterator over tokens and constructs a list, that when passed to
# itertools.product, will produce an iterator over the output lines. References
# are not taken, but are stored so that they can be done later.
################################################################################
def Parse(itoken):
	toplevel = []
	listlevel = []
	rangelevel = []
	reflevel = []

	for token in itoken:
		# the following print statement is DEBUG code
		print '{:13} | {:10} | {:4} | \'{}\''.format(token[0], token[2], token[3], token[1])

		# if an unexpected character is encountered, 
		if (token[0] == 'UNEXPECTED'):
			print >> sys.stderr, "Syntax error: Unexpected '{}' at position {} in context '{}'".format(token[1], token[3], token[2])
			return None

		# deal with normal strings appearing at the top level
		elif (token[0] == 'NORMAL' and token[2] == 'top'):
			toplevel.append(iter([token[1]]))

		# deal with tokens appearing in list context
		elif (token[2] == 'list'):
			listlevel.append(token)
		#deal with end of list
		elif (token[0] == 'LIST_CLOSE'):
			toplevel.append(itertools.imap(lambda x: x[1], itertools.ifilter(lambda x: x[0]=='NORMAL', listlevel)))
			listlevel = []

		#deal with tokens in range context
		elif (token[2] == 'range'):
			rangelevel.append(token)
		#deal with end of range
		elif (token[0] == 'RANGE_CLOSE'):

			rangelevel = []

	return toplevel

