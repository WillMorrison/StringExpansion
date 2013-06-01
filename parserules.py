from itertools import chain
from lexrules import tokens
from NumRange import NumRange
from Enumerator import Enumerator

# this takes an expression (stored as a tuple containing two lists) and turns it into
# a generator that returns the values
def p_finalizedexpression(p):
	'''finalizedexpression : expression'''
	#p[0] = p[1]
	p[0] = Enumerator(p[1][0], p[1][1])

# this defines an expression from the concatenation of lists, ranges, and strings
# references are handled separately
def p_expression(p):
	'''expression : expression string
	              | expression range
	              | expression list
	              | string
	              | list
	              | range'''
	if len(p) == 2:
		p[0] = ( [p[1]], [0] )
	elif len(p) == 3:
		p[0] = ( p[1][0] + [p[2]], p[1][1] + [len(p[1][0])] )

# this handles references in expressions
def p_expression_ref(p):
	''' expression : expression ref'''
	p[0] = ( p[1][0], p[1][1] + [p[2]] )

# This rule will concatenate adjacent strings into one
def p_string(p):
	'''string : STRING string
	          | ESCCHAR string
	          | QUOTEDSTRING string
	          | STRING
	          | ESCCHAR
	          | QUOTEDSTRING'''
	if len(p) == 2:
		p[0] = [ p[1] ]
	elif len(p) == 3:
		p[0] = [ p[1] + p[2][0] ]

# This rule defines numerical ranges
def p_range(p):
	'''range : LBRACKET NUMBER HYPHEN NUMBER RBRACKET
	         | LBRACKET NUMBER HYPHEN NUMBER COLON NUMBER RBRACKET'''
	
	if len(p) == 6:
		p[0] = NumRange(p[2], p[4])
	elif len(p) == 8:
		p[0] = NumRange(p[2], p[4], int(p[6]))

# this defines a reference
def p_ref(p):
	'''ref : LPAREN NUMBER RPAREN'''
	p[0] = int(p[2]) - 1

# this defines a list
def p_list(p):
	'''list : LBRACE listitems RBRACE'''
	p[0] = p[2]

# this defines the items inside a list
def p_listitems(p):
	'''listitems : finalizedexpression COMMA listitems
	             | finalizedexpression'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = chain(p[1], p[3])
