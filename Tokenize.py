import itertools

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
			if (len(normalchars) > 0):
				yield ('NORMAL',''.join(normalchars), context[-1], position)
				normalchars = []
			context.append('string')
		# close a quoted string
		# string may be empty, so we will ALWAYS return a normal
		elif (context[-1] in ['string'] and char == '"'): 
			context.pop()
			yield ('NORMAL',''.join(normalchars), context[-1], position)
			normalchars = []
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
