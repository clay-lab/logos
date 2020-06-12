# generate_forms.py
#
# Generates a TSV file containing sentences and their logical forms generated
# from the provided featural context-free grammar.

import nltk
from nltk.parse.generate import generate
from nltk.grammar import FeatureGrammar

def generate_f(grammar_file, out_file):

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
				o.write(string)

if __name__ == '__main__':
	generate_f('grammar.fcfg', 'forms.txt')