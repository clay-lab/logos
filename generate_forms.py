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

from nltk import CFG, Tree

import tree as TREE

import sys
import re
				
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

def _generate_forms(sentences: List, grammar: str, format):
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
		for (syntree, semrep) in result:
			# print(syntree)
			representations.append((str(syntree), '{0}'.format(semrep)))

	if representations and format == 'tree':
		g = nltk.data.load('./grammars/predicate.cfg', 'cfg')
		parser = nltk.parse.BottomUpChartParser(g)
		tree = TREE.string_to_tree(representations[0][1], parser)
		outstring = ' '.join(str(tree).replace('\n', '').split())
		return [(representations[0][1], outstring)]

	return representations

def get_forms(grammar_file: str, experiment: str, format: str):
	"""
	Generates all sentences derivable from the provided FCFG and writes them out
	to a TSV file along with their interpreted semantic representation.

	@param grammar_file: Path to file containing the FCFG.
	@param experiment: Path to the file where the TSV data will be written. Note 
		that this file will be overridden on every run.
	"""

	experiment_dir = os.path.join('experiments', experiment)

	if not os.path.isdir(experiment_dir):
		print('Creating directory {0}'.format(experiment_dir))
		os.mkdir(experiment_dir)

	data_dir = os.path.join(experiment_dir, 'data')

	if not os.path.isdir(data_dir):
		print('Creating data directory {0}'.format(data_dir))
		os.mkdir(data_dir)

	sentences = []
	outpath = os.path.join(data_dir, experiment + '.forms')
	grammar_path = os.path.join('grammars', grammar_file + '.fcfg')

	with open(grammar_path, 'r') as g:

		contents = g.readlines()
		grammar = FeatureGrammar.fromstring(contents)

		for sentence in generate(grammar):
			sentences.append(' '.join(sentence).strip())

	with open(outpath, 'w') as o:
		o.write('source\ttransformation\ttarget\n')
		with tqdm(sentences) as t:
			for s in t:
				result = _generate_forms([s], grammar_path, format)
				if result:
					syn, sem = result[0]
					o.write('{0}\tsem\t{1}\n'.format(s, sem))

def get_splits(splits: Dict, experiment: str, excluded: List, testing: List):
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

	experiment_dir = os.path.join('experiments', experiment)

	if testing is not None and testing != []:
		test_pattern = {}
		for t in testing:
			name, pattern = t.split(':')
			test_pattern[name] = pattern
	else:
		test_pattern = None

	# if excluded is not None and excluded != []:
	# 	exclude_pattern = {}
	# 	for x in excluded:
	# 		name, pattern = x.split(':')
	# 		exclude_pattern[name] = pattern
	# else:
	# 	exclude_pattern = None

	if not os.path.isdir(experiment_dir):
		print('Creating directory {0}'.format(experiment_dir))
		os.mkdir(experiment_dir)

	data_dir = os.path.join(experiment_dir, 'data')

	if not os.path.isdir(data_dir):
		print('Creating data directory {0}'.format(data_dir))
		os.mkdir(data_dir)

	with open(os.path.join(data_dir, 'args'), 'w') as argsfile:
		argsfile.write(' '.join(sys.argv))

	if test_pattern is not None:
		for k, v in test_pattern.items():
			with open(os.path.join(data_dir, k + '.test'), 'w') as f:
				f.write('source\ttransformation\ttarget\n')

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
	basefile = os.path.join(data_dir, experiment + '.forms')
	with open(basefile, 'r') as f:
		for i, _ in enumerate(f):
			pass
		lines = i + 1

	results = np.random.choice(keys, lines, p = values)
	for key in keys:
		with open(os.path.join(data_dir, '{0}.{1}'.format(experiment, key)), 'w') as kf:
			kf.write('source\ttransformation\ttarget\n')

	
	with open(basefile, 'r') as f:
		for i, line in enumerate(f):
			if i == 0: 
				pass
			else:
				# Create train/val/test splits 
				outfile = '{0}.{1}'.format(experiment, results[i])
				if excluded is not None:
					for pattern in excluded:
						if re.search(pattern, line, re.IGNORECASE):
							outfile = '{0}.test'.format(experiment)
							break
				with open(os.path.join(data_dir, outfile), 'a') as o:
					o.write(line)

				# Create separate test files
				if test_pattern is not None:
					for key, pattern in test_pattern.items():
						if re.search(pattern, line, re.IGNORECASE):
							tfile = '{0}.test'.format(key)
							with open(os.path.join(data_dir, tfile), 'a') as o:
								o.write(line)


