import itertools

def Enumerator(expressions, expansionmap):
	"""
	An enumerator takes a sequence of iterables and an indexable sequence.
	It computes the cartesian product of the iterables, then expands each result using the expansion map.
	"""
	for sentence in itertools.product(*expressions):
		yield ''.join(map (lambda i: sentence[i], expansionmap) )
