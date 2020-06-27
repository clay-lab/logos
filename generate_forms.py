# generate_forms.py
#
# Generates a TSV file containing sentences and their logical forms generated
# from the provided featural context-free grammar.

import nltk
from nltk.parse.generate import generate
from nltk.grammar import FeatureGrammar
from nltk.sem.logic import ApplicationExpression, LambdaExpression, AbstractVariableExpression, QuantifiedExpression, BinaryExpression, Tokens, BooleanExpression
from typing import List, Dict
import numpy as np
import os
from tqdm import tqdm
				
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

def _generate_forms(sentences: List, grammar: str):
	"""
	Generates semantic representations for the provided sentences.

	@param sentences: A List of strings
	@returns: A List of representations
	"""

	swizzle()

	representations = []

	# s = []
	# s.append(sentences[0])
	# s.append(sentences[0])
	# s.append(sentences[0])

	# nltk.interpret_sents(s, grammar)

	for i, result in enumerate(nltk.interpret_sents(sentences, grammar)):
		for (_, semrep) in result:
			representations.append('{0}'.format(semrep))

	return representations

def get_forms(grammar_file: str, task: str):
	"""
	Generates all sentences derivable from the provided FCFG and writes them out
	to a TSV file along with their interpreted semantic representation.

	@param grammar_file: Path to file containing the FCFG.
	@param task: Path to the file where the TSV data will be written. Note 
		that this file will be overridden on every run.
	"""

	sentences = []
	outpath = os.path.join('splits', task + '.forms')
	grammar_path = os.path.join('grammars', grammar_file)

	with open(grammar_path, 'r') as g:

		contents = g.readlines()
		grammar = FeatureGrammar.fromstring(contents)

		for sentence in generate(grammar):
			sentences.append(' '.join(sentence).strip())

	with open(outpath, 'w') as o:
		o.write('source\ttransformation\ttarget\n')
		with tqdm(sentences) as t:
			for s in t:
				result = _generate_forms([s], grammar_path)
				if result:
					o.write('{0}\tsem\t{1}\n'.format(s, result[0]))

def get_splits(splits: Dict, task: str):
	"""
	Splits the input file into n different files based on the values provided in
	the splits parameter. This is a dictionary of the form
	{
		"split_name": percent
	}
	where 0 <= percent <= 1 and the sum of all percent values in the dictionary
	is 1.0. This will yield a new file named
	
	semantics.split_name

	containing `percent` of the total lines in basefile. It is guaranteed that
	all generated files are disjoint.

	@param splits: Dictionary of splits and percentages.
	@param basefile: File to generate splits from.
	"""

	total = 0.0
	values = []
	keys = []
	for split in splits.items():
		key, value = split
		if value < 0:
			print("Split percentages must be non-negative")
			raise(SystemError)
		total += value
		keys.append(key)
		values.append(value)

	if total > 1:
		print("Split percentages must sum to 1.0")
		raise(SystemError)

	lines = 0
	basefile = os.path.join('splits', task + '.forms')
	with open(basefile, 'r') as f:
		for i, _ in enumerate(f):
			pass
		lines = i + 1

	results = np.random.choice(keys, lines, p = values)
	for key in keys:
		with open(os.path.join('splits', '{0}.{1}'.format(task, key)), 'w') as kf:
			kf.write('source\ttransformation\ttarget\n')

	with open(basefile, 'r') as f:
		for i, line in enumerate(f):
			if i == 0: 
				pass
			else:
				with open(os.path.join('splits', '{0}.{1}'.format(task, results[i])), 'a') as o:
					o.write(line)
