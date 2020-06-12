# generate_forms.py
#
# This is the main file for the Logos project, a model which aims to translate
# input sequences of natural language into logical forms, either ouput as 
# sequences of some formal logic or as trees.

import nltk
from nltk.parse.generate import generate
from nltk.grammar import FeatureGrammar

def generate_f(grammar_file, out_file):

	sentences = []

	with open(grammar_file, 'r') as g:

		contents = g.readlines()
		grammar = FeatureGrammar.fromstring(contents)

		for sentence in generate(grammar):
			sentences.append(' '.join(sentence))

	with open(out_file, 'w') as o:
		for i, result in enumerate(nltk.interpret_sents(sentences, grammar_file)):
			# print(result)
			# type(type(result))
			for (synrep, semrep) in result:
				# s = semrep.uncurry()
				# print(s)
				# raise(SystemError)

				# print(type(semrep))
				# print('{0}'.format(semrep))
				string = sentences[i].strip() + '\t' + '{0}'.format(semrep) + '\n'
				o.write(string)

if __name__ == '__main__':
	generate_f('grammar.fcfg', 'forms.txt')