import sys
import re

# the explicit states for the lexer, there is also an implicit INITIAL state
states = (('list', 'inclusive'), ('range', 'exclusive'), ('ref', 'exclusive'))

# This is a complete list of token types for all states
tokens = (
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'LBRACKET',
	'RBRACKET',
	'ESCCHAR',
	'QUOTEDSTRING',
	'STRING',
	'HYPHEN',
	'COLON',
	'COMMA',
	'NUMBER'
)

#######################################
# Expressions for tokens in INITIAL context 
#######################################

t_STRING = r'[^"[{(\\]+'

def t_QUOTEDSTRING(t):
	r'"(\\.|[^"])+"'
	t.value = re.sub(r'\\(.)', r'\1', t.value[1:-1])
	return t

def t_LPAREN(t):
	r'\('
	t.lexer.push_state('ref')
	return t

def t_LBRACE(t):
	r'{'
	t.lexer.push_state('list')
	return t

def t_LBRACKET(t):
	r'\['
	t.lexer.push_state('range')
	return t

def t_ESCCHAR(t):
	r'\\.'
	t.value = t.value[1]
	return t

def t_LQUOTE(t):
	r'"'
	t.lexer.push_state('string')

def t_error(t):
	print ("Illegal character '{}' at position {}".format(t.value[0], t.lexer.lexpos), file=sys.stderr)
	t.lexer.skip(1)

#######################################
# Expressions for tokens in list context
# This is an inclusive state, expressions from INITIAL are also active
#######################################

t_list_STRING = r'[^,"[{}(\\]+'
t_list_COMMA = r','
def t_list_RBRACE(t):
	r'}'
	t.lexer.pop_state()
	return t

#######################################
# Expressions for tokens in range context
# This state is exclusive, only the following tokens are recognized
#######################################
t_range_HYPHEN = r'-'
t_range_COLON = r':'
t_range_NUMBER = r'\d+'

def t_range_RBRACKET(t):
	r']'
	t.lexer.pop_state()
	return t

def t_range_error(t):
	print ("Illegal character '{}' at position {}".format(t.value[0], t.lexer.lexpos), file=sys.stderr)
	t.lexer.skip(1)
	

#######################################
# Expressions for tokens in ref context
# This state is exclusive, only the following tokens are recognized
#######################################
t_ref_NUMBER = r'\d+'

def t_ref_RPAREN(t):
	r'\)'
	t.lexer.pop_state()
	return t

def t_ref_error(t):
	print ("Illegal character '{}' at position {}".format(t.value[0], t.lexer.lexpos), file=sys.stderr)
	t.lexer.skip(1)
