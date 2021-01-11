import os
from nltk import parse, interpret_sents
from nltk.grammar import FeatureGrammar
from pcfg import PCFG
from generate_forms import swizzle
import itertools

def main():

  swizzle()

  gen_file_path = "grammars/intervening.pcfg"
  sem_file_path = "grammars/turtle.fcfg"

  TEST_SENTENCE = "the queen near Bob sees Alice"

  with open(gen_file_path, 'r') as gen:
    gen_grammar = PCFG.fromstring(gen.readlines())

    with open(sem_file_path, 'r') as sem:
      sem_grammar = FeatureGrammar.fromstring(sem.readlines())

      # for sentence in gen_grammar.generate(10):

        # print(sentence)
        
      result = interpret_sents([TEST_SENTENCE], sem_grammar)
      if list(itertools.chain(*result)):
        print(f'{TEST_SENTENCE} → {result[0][0][-1]}')

if __name__ == "__main__":
  main()