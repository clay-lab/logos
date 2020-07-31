# tree.py
# 
# Parses semrep outputs into trees.

import nltk
from nltk import CFG, Tree, ParentedTree
from nltk.treetransforms import collapse_unary

read_expr = nltk.sem.Expression.fromstring


def collapse_unary(tree, collapsePOS=False, collapseRoot=False):
    """
    Collapse subtrees with a single child (ie. unary productions)
    into a new non-terminal (Tree node) joined by 'joinChar'.
    This is useful when working with algorithms that do not allow
    unary productions, and completely removing the unary productions
    would require loss of useful information.  The Tree is modified
    directly (since it is passed by reference) and no value is returned.

    :param tree: The Tree to be collapsed
    :type  tree: Tree
    :param collapsePOS: 'False' (default) will not collapse the parent of leaf nodes (ie.
                        Part-of-Speech tags) since they are always unary productions
    :type  collapsePOS: bool
    :param collapseRoot: 'False' (default) will not modify the root production
                         if it is unary.  For the Penn WSJ treebank corpus, this corresponds
                         to the TOP -> productions.
    :type collapseRoot: bool
    :param joinChar: A string used to connect collapsed node values (default = "+")
    :type  joinChar: str
    """

    if collapseRoot == False and isinstance(tree, Tree) and len(tree) == 1:
        nodeList = [tree[0]]
    else:
        nodeList = [tree]

    # depth-first traversal of tree
    while nodeList != []:
        node = nodeList.pop()
        if isinstance(node, Tree):
            if (
                len(node) == 1
                and isinstance(node[0], Tree)
                and (collapsePOS == True or isinstance(node[0, 0], Tree))
            ):
                # node.set_label(node.label())
                node[0:] = [child for child in node[0]]
                node = node.label()
                # since we assigned the child's children to the current node,
                # evaluate the current node again
                nodeList.append(node)
            else:
                for child in node:
                    nodeList.append(child)

def unary_to_leaf(tree):
	"""
	Turns unary subtrees into leaves
	"""

	nodeList = [tree]

	while nodeList != []:
		node = nodeList.pop()
		if isinstance(node, Tree) and node.height() == 2:
			print('Pruning: ', node)
			print('What I see: ', node.height())
			node = node[0]
			print('Node is now:', node)
		else:
			for child in node:
				nodeList.append(child)


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

def trim(tree):	

	# Remove all extraneous nodes
	for sub in reversed(list(tree.subtrees())):
		if sub.label() in ['R_PAREN', 'L_PAREN', 'COMMA']:
			parent = sub.parent()
			while parent and len(parent) == 1:
				sub = parent
				parent = sub.parent()
			# print(sub, "will be deleted")
			del tree[sub.treeposition()]

	# Replace unary trees with leaves
	collapse_unary(tree, collapsePOS=True, collapseRoot=True)
	for sub in reversed(list(tree.subtrees())):
		if len(sub.leaves()) == 1:
			leaf = sub[0]
			tree[sub.treeposition()] = leaf


def flat_tree(parse) -> str:
	for tree in parse:
		tree_str = ' '.join(str(tree).split())
		# print(tree_str)
		return tree_str

def string_to_tree(string, parser):
	string = string.replace('(', '[').replace(')', ']')
	parsed_string = parser.parse(string.split())
	tst = flat_tree(parsed_string)
	tree = ParentedTree.fromstring(tst)
	trim(tree)
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



if __name__ == '__main__':
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
	parser = nltk.parse.BottomUpChartParser(grammar)

	alice_alice_str = '( see alice alice )'
	alice_bob_str = '(see alice bob )'

	for s in [alice_alice_str, alice_bob_str]:

		tree = string_to_tree(s, parser)
		flat = str(tree).replace('\n', '').split()
		print(' '.join(flat))
		# print(flat_tree(tree))

		tree.collapse_unary()

		for subtree in tree.subtrees(filter = lambda t: t.label() in ['DOT', 'L_PAREN', 'R_PAREN', 'COMMA']):
			for n, c in enumerate(subtree):
				subtree[n] = ''

		# prefix_binops(tree)
		# print(flat_tree(tree))

		print(tree_to_expstring(tree))
