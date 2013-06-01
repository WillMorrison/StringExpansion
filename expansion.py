import sys

import lexrules
import parserules

import ply.lex as lex
import ply.yacc as yacc

lexer = lex.lex(module=lexrules)
parser = yacc.yacc(module=parserules)

result = parser.parse(sys.argv[1], lexer=lexer)
for line in result:
	print(line)
