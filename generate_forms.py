# generate_forms.py
#
# Generates a TSV file containing sentences and their logical forms generated
# from the provided featural context-free grammar.

import nltk
from nltk.parse.generate import generate
from nltk.grammar import FeatureGrammar
from nltk.sem.logic import ApplicationExpression, LambdaExpression, AbstractVariableExpression, QuantifiedExpression, BinaryExpression, Tokens, BooleanExpression
				

def swizzle():
	"""
	Add new formatting methods to expressions so that their string 
	representations have spaces around tokens.
	"""

	def __str_formatted__(self):
		# uncurry the arguments and find the base function
		if self.is_atom():
			function, args = self.uncurry()
			arg_str = ", ".join("%s" % arg for arg in args)
		else:
			# Leave arguments curried
			function = self.function
			arg_str = "%s" % self.argument

		function_str = "%s" % function
		parenthesize_function = False
		if isinstance(function, LambdaExpression):
			if isinstance(function.term, ApplicationExpression):
				if not isinstance(function.term.function, AbstractVariableExpression):
					parenthesize_function = True
			elif not isinstance(function.term, BooleanExpression):
				parenthesize_function = True
		elif isinstance(function, ApplicationExpression):
			parenthesize_function = True	

		if parenthesize_function:
			function_str = Tokens.OPEN + function_str + Tokens.CLOSE

		return function_str + Tokens.OPEN + " " + arg_str + Tokens.CLOSE

	def __var_str_formatted__(self):
		return "%s " % self.variable

	def __lambda_str_formatted__(self):
		variables = [self.variable]
		term = self.term
		while term.__class__ == self.__class__:
			variables.append(term.variable)
			term = term.term
		return (
			Tokens.LAMBDA
			+ " ".join("%s" % v for v in variables)
			+ " "
			+ Tokens.DOT
			+ " %s " % term
		)

	def __quantified_str_formatter__(self):
		variables = [self.variable]
		term = self.term
		while term.__class__ == self.__class__:
			variables.append(term.variable)
			term = term.term
		return (
			self.getQuantifier()
			+ " "
			+ " ".join("%s" % v for v in variables)
			+ " "
			+ Tokens.DOT
			+ " %s" % term
		)

	def __binary_str_formatted__(self):
		first = self._str_subex(self.first)
		second = self._str_subex(self.second)
		return Tokens.OPEN + " " + first + " " + self.getOp() + " " + second + " " + Tokens.CLOSE

	ApplicationExpression.__str__ = __str_formatted__
	AbstractVariableExpression.__str__ = __var_str_formatted__
	LambdaExpression.__str__ = __lambda_str_formatted__
	QuantifiedExpression.__str__ = __quantified_str_formatter__
	BinaryExpression.__str__ = __binary_str_formatted__

def generate_f(grammar_file: str, out_file: str):
	"""
	Generates all sentences derivable from the provided FCFG and writes them out
	to a TSV file along with their interpreted semantic representation.

	@param grammar_file: Path to file containing the FCFG.
	@param out_file: Path to the file where the TSV data will be written. Note 
		that this file will be overridden on every run.
	"""

	swizzle()

	sentences = []

	with open(grammar_file, 'r') as g:

		contents = g.readlines()
		grammar = FeatureGrammar.fromstring(contents)

		for sentence in generate(grammar):
			sentences.append(' '.join(sentence).strip())

	with open(out_file, 'w') as o:
		for i, result in enumerate(nltk.interpret_sents(sentences, grammar_file)):
			for (synrep, semrep) in result:
				string = sentences[i] + '\t' + '{0}'.format(semrep) + '\n'
				print('{0}'.format(semrep))
				o.write(string)