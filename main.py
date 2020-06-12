import argparse
import generate_forms

def getArguments():
	"""
	Instantiates an arugment parser, parses the command line arguments,
	and returns them.

	@return: args (argparse.Namespace) - command line arguments
	"""
	parser = argparse.ArgumentParser(description = 'Translate sentences into logical forms.')
	parser.add_argument(
		'-g', '--grammar',
		type = str,
		help = 'file containing grammar (FCFG) to generate logical forms',
		default = 'grammar.fcfg'
	)
	parser.add_argument(
		'-o', '--output',
		type = str,
		help = 'output file',
		default = 'forms.txt'
	)

	args = parser.parse_args()
	return args

def main():

	args = getArguments()
	generate_forms.generate_f(args.grammar, args.output)

if __name__ == '__main__':
	main()