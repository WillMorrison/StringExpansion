import itertools
import sys
import NumRange

################################################################################
# Purpose: Turn a list of tokens into two lists. The first list is designed to 
#          be passed to itertools.product, and the second list will be used to
#          perform references on the tuples returned by itertools.product.
#
# Arguments: one iterator over tokens
#
# Returns: Two lists, a list of iterables and a reference map
################################################################################
def Parse(itoken):
	toplevel = []
	listlevel = []
	rangelevel = []
	reflevel = []
	expansionmap = []

	for token in itoken:
		# the following print statement is DEBUG code
		print '{:13} | {:10} | {:4} | \'{}\''.format(token[0], token[2], token[3], token[1])

		# if an unexpected character is encountered, 
		if (token[0] == 'UNEXPECTED'):
			print >> sys.stderr, "Syntax error: Unexpected '{}' at position {} in context '{}'".format(token[1], token[3], token[2])
			return None, None

		# deal with normal strings appearing at the top level
		elif (token[0] == 'NORMAL' and token[2] == 'top'):
			toplevel.append([token[1]])
			expansionmap.append(len(toplevel))

		# deal with tokens appearing in list context
		elif (token[2] == 'list'):
			listlevel.append(token)
		#deal with end of list
		elif (token[0] == 'LIST_CLOSE'):
			toplevel.append(map(lambda x: x[1], filter(lambda x: x[0]=='NORMAL', listlevel)))
			expansionmap.append(len(toplevel))
			listlevel = []

		#deal with tokens in range context
		elif (token[2] == 'range'):
			rangelevel.append(token)
		#deal with end of range
		elif (token[0] == 'RANGE_CLOSE'):
			# check that we have the correct number of arguments
			numbers = filter(lambda x: x[0]=='NUMBER', rangelevel)
			if len(numbers) is 2:
				seq = map(lambda x: x[1], numbers)
			elif len(numbers) is 3:
				seq = map(lambda x: x[1], numbers[0:1]) + int(numbers[2][1])
			else:
				print >> sys.stderr, "Syntax error: Incorrect number of elements in range ending at position {}".format(token[3])
				return None, None

			# construct a range here and append it to toplevel or listlevel
			if (token[2] == 'top'):
				toplevel.append(NumRange.NumRange(*seq))
				expansionmap.append(len(toplevel))
			elif(token[2] == 'list'):
				listlevel.append(NumRange.NumRange(*seq))
			rangelevel = []

		#deal with tokens in ref context
		elif (token[2] == 'reference'):
			reflevel.append(token)
		#deal with end of range
		elif (token[0] == 'REF_CLOSE'):
			# check that we have the correct number of arguments
			numbers = filter(lambda x: x[0]=='NUMBER', reflevel)
			if len(numbers) is not 1:
				print >> sys.stderr, "Syntax error: Multiple elements in reference ending at position {}".format(token[3])
				return None, None

			expansionmap.append(int(numbers[0][1]))
			reflevel = []

	return toplevel, expansionmap

