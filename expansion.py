import itertools
import sys

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


################################################################################
# This function will tokenize the expression into normal strings and special
# characters. It consists of a state machine with an associated context stack.
################################################################################
def Tokenize( expression ):
	normalchars = []
	context = ['top']
	position = 0

	for char in expression:
		position+=1

		# if this character is an escape character, escape the next character
		if (context[-1] in ['top','string','list'] and char == '\\'):
			context.append('escaped')
		# if the previous character was an escape char
		elif (context[-1] in ['escaped']):
			normalchars.append(char)
			context.pop()

		# open a quoted string
		elif (context[-1] in ['top','list'] and char == '"'):
			context.append('string')
		# close a quoted string
		elif (context[-1] in ['string'] and char == '"'): 
			context.pop()
		# other characters are appended to current normal
		elif (context[-1] in ['string']):
			normalchars.append(char)

		# open a range
		elif (context[-1] in ['top','list'] and char == '['):
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			yield ('RANGE_OPEN',char, context[-1], position)
			context.append('range')
		# delimit a range
		elif (context[-1] in ['range'] and char == ':'):
			if (len(normalchars) > 0):
				yield ('NUMBER',''.join(normalchars), context[-1], position)
				normalchars = []
			yield ('RANGE_DELIMIT',char, context[-1], position)
		# close a range
		elif (context[-1] in ['range'] and char == ']'):
			if (len(normalchars) > 0):
				yield ('NUMBER',''.join(normalchars), context[-1], position)
				normalchars = []
			context.pop()
			yield ('RANGE_CLOSE',char, context[-1], position)
		# numeric characters are appended to current number
		elif (context[-1] in ['range'] and char.isdigit()):
			normalchars.append(char)

		# open a reference
		elif (context[-1] in ['top'] and char == '('):
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			yield ('REF_OPEN',char, context[-1], position)
			context.append('reference')
		# close a reference
		elif (context[-1] in ['reference'] and char == ')'):
			if (len(normalchars) > 0):
				yield ('NUMBER',''.join(normalchars), context[-1], position)
				normalchars = []
			context.pop()
			yield ('REF_CLOSE',char, context[-1], position)
		# numeric characters are appended to current number
		elif (context[-1] in ['reference'] and char.isdigit()):
			normalchars.append(char)
			
		# open a list
		elif (context[-1] in ['top'] and char == '{'):
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			yield ('LIST_OPEN',char, context[-1], position)
			context.append('list')
		# delimit a list
		elif (context[-1] in ['list'] and char == ','):
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			yield ('LIST_DELIMIT',char, context[-1], position)
		# close a list
		elif (context[-1] in ['list'] and char == '}'):
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			context.pop()
			yield ('LIST_CLOSE',char, context[-1], position)
		# numeric characters are appended to current number
		elif (context[-1] in ['list']):
			normalchars.append(char)

		# top level may have any character
		elif (context[-1] in ['top']):
			normalchars.append(char)

		# all other characters are unexpected
		else:
			yield ('UNEXPECTED', char, context[-1], position)

	# we have reached the end of the string, yield any remaining normal/number characters
	if (len(normalchars) > 0 and context[-1] in ['reference', 'range']):
		yield ('NUMBER',''.join(normalchars), context[-1], position)
	elif (len(normalchars) > 0):
		yield ('NORMAL',''.join(normalchars), context[-1], position)

	# Is context sane?
	if (context != ['top']):
		yield ('UNEXPECTED', 'EOF', context[-1], position)


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



if (len(sys.argv) > 1):
	lines = Parse(Tokenize(sys.argv[1]))
	if (lines is not None):
		for line in lines:
			print ','.join(line)
else:
	print >> sys.stderr, "Error: An argument is required"

#if (len(sys.argv) > 1):
#	for token in Tokenize(sys.argv[1]):
#		print '{:13} | {:10} | {:4} | \'{}\''.format(token[0], token[2], token[3], token[1])
#else:
#	print "Error, argument required"
