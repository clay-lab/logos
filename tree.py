# tree.py
# 
# Parses semrep outputs into trees.

import nltk
from nltk import CFG, Tree

read_expr = nltk.sem.Expression.fromstring

alice_str = 'see ( alice , alice )' 
# ( see alice alice )
turtle_str = 'all x . ( ( person ( x ) & near ( x , victor ) ) -> notice ( x , neha ) )' 
"""
( forall 
	x 
	( -> 
		( & 
			( person x ) 
			( near x victor ) ) 
		( notice x neha ) ) )
"""

# alice = read_expr(alice_str)
# print(alice)

# turtle = read_expr(turtle_str)
# print(turtle)


grammar = CFG.fromstring("""
EXP -> OP L_PAREN EXP R_PAREN | OP L_PAREN EXP COMMA EXP R_PAREN | EXP AND EXP | EXP IMPL EXP | VAR
OP -> Q VAR DOT

# Terminals
L_PAREN -> '['
R_PAREN -> ']'
COMMA -> ','
AND -> '&'
IMPL -> '->'
DOT -> '.'

Q -> 'all'
OP -> 'see' | 'meet' | 'like' | 'dislike' | 'throw' | 'notice' | 'know' | 'walk' | 'sleep' | 'eat' | 'run' | 'sing' | 'dance' | 'fly' | 'slumber'
VAR -> 'x' | 'alice' | 'bob' | 'claire' | 'daniel' | 'eliza' | 'francis' | 'grace' | 'henry' | 'isla' | 'john' | 'katherine' | 'lewis' | 'margaret' | 'neha' | 'oswald' | 'patricia' | 'quinn' | 'rachael' | 'samuel' | 'tracy' | 'ursula' | 'victor' | 'winnifred' | 'xerxes' | 'yvettte' | 'zelda'
""")

def prefix_binops(tree):
	"""
		Converts subtrees involving binary operators (&, ->) to prefix notation.
	"""

	for node in tree:
		if type(node) is Tree:
			# print('I am a', node.label())
			# print('\t My children are:')
			for st in node:
				if '&' in st:
					print('I am a', node.label())
					print(st)
			prefix_binops(node)			

def flat_tree(parse) -> str:
	for tree in parse:
		tree_str = ' '.join(str(tree).split())

	return tree_str

def string_to_tree(string, parser):
	# parser = nltk.parse.BottomUpChartParser(grammar)
	string = string.replace('(', '[').replace(')', ']')
	parsed_string = parser.parse(string.split())
	tree_str = flat_tree(parsed_string)
	tree = Tree.fromstring(tree_str)

	return tree

def tree_to_expstring(tree):
	"""
	Converts a tree into the expression syntax that is used to represent the
	predicate logic for our semantics.

	The following must be done in order to make the expression valid:
		(1) Insert L_PAREN immediately after every OP node and R_PAREN after the
			last child on OP's level.
		(2) Insert COMMAs between two or more arguments
		(2) Move binary operators (&, |, ->) to infix notation.
		(3) Change the parenthesis from angle brackets to parens.
	"""

	for i, subtree in enumerate(tree.subtrees()):
		if subtree.label() == 'L_PAREN':
			for n, c in enumerate(subtree):
				subtree[n] = '['
		elif subtree.label() == 'R_PAREN':
			for n, c in enumerate(subtree):
				subtree[n] = ']'
		elif subtree.label() == 'COMMA':
			for n, c in enumerate(subtree):
				subtree[n] = ','

	tree_str = ' '.join(filter(lambda s: s != '', tree.leaves())).replace('[', '(').replace(']', ')')
	return tree_str



# for s in [alice_str, turtle_str]:

# 	tree = string_to_tree(s)
# 	flat = str(tree).replace('\n', '').split()
# 	print(' '.join(flat))
# 	# print(flat_tree(tree))

# 	tree.collapse_unary()

# 	for subtree in tree.subtrees(filter = lambda t: t.label() in ['DOT', 'L_PAREN', 'R_PAREN', 'COMMA']):
# 		for n, c in enumerate(subtree):
# 			subtree[n] = ''

# 	# prefix_binops(tree)
# 	# print(flat_tree(tree))

# 	print(tree_to_expstring(tree))
