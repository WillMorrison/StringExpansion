import sys
import Tokenize

if (len(sys.argv) > 1):
	print '{:13} | {:10} | {:8} | {}'.format('Token', 'Context', 'Position', 'Contents')
	print '--------------+------------+----------+----------'
	for token in Tokenize.Tokenize(sys.argv[1]):
		print '{:13} | {:10} | {:8} | \'{}\''.format(token[0], token[2], token[3], token[1])
else:
	print "Error, argument required"
