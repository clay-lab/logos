import unittest
import generate_forms

class TestParsing(unittest.TestCase):

	grammar_file = 'grammar.fcfg'

	def test_intransitive(self):
		sentences = [
			"Alice walks",
			"Everyone walks",
			"Someone walks"
		]
		target = [
			"walk ( alice )",
			"all x . ( person ( x ) -> walk ( x ) )",
			"exists x . ( person ( x ) & walk ( x ) )"
		]
		self.assertEqual(target, generate_forms._generate_forms(sentences, self.grammar_file))

	def test_transitive(self):
		sentences = [
			"Claire sees Alice",
			"Claire sees Everyone",
			"Claire sees Someone",
			"Everyone sees Claire",
			"Someone sees Claire"
		]
		target = [
			"see ( claire , alice )",
			"all x . ( person ( x ) -> see ( claire , x ) )",
			"exists x . ( person ( x ) & see ( claire , x ) )",
			"all x . ( person ( x ) -> see ( x , claire ) )",
			"exists x . ( person ( x ) & see ( x , claire ) )"	
		]
		self.assertEqual(target, generate_forms._generate_forms(sentences, self.grammar_file))

if __name__ == '__main__':
	unittest.main()