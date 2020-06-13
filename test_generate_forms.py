import unittest
import generate_forms
import os

class TestParsing(unittest.TestCase):

	grammar_file = 'grammar.fcfg'
	out_file = 'testing.txt'

	def test_intransitive(self):
		"""
		Checks intransitive sentences.
		"""
		rubric = [
			("Alice walks", "walk ( alice )"),
			("Everyone walks", "all x . ( person ( x ) -> walk ( x ) )"),
			("Someone walks", "exists x . ( person ( x ) & walk ( x ) )")
		]
		self.assertEqual(
			[r[1] for r in rubric], 
			generate_forms._generate_forms([r[0] for r in rubric], self.grammar_file)
		)

	def test_transitive(self):
		"""
		Checks transitive sentences.
		"""
		rubric = [
			("Claire sees Alice", "see ( claire , alice )"),
			("Claire sees Everyone", "all x . ( person ( x ) -> see ( claire , x ) )"),
			("Claire sees Someone", "exists x . ( person ( x ) & see ( claire , x ) )"),
			("Everyone sees Claire", "all x . ( person ( x ) -> see ( x , claire ) )"),
			("Someone sees Claire", "exists x . ( person ( x ) & see ( x , claire ) )"),
			("Bob sees Himself", "see ( bob , bob )"),
			("Everyone sees Himself", "all x . ( person ( x ) -> see ( x , x ) )"),
			("Someone sees Himself", "exists x . ( person ( x ) & see ( x , x ) )")
		]
		self.assertEqual(
			[r[1] for r in rubric], 
			generate_forms._generate_forms([r[0] for r in rubric], self.grammar_file)
		)

	def test_whitespace(self):
		"""
		Checks for extranous whitespace or formatting in the generate output file.
		"""
		generate_forms.generate_f(self.grammar_file, self.out_file)
		with open(self.out_file, 'r') as f:
			contents = f.readlines()
			self.assertNotIn('  ', contents)
		os.remove(self.out_file)

if __name__ == '__main__':
	unittest.main()