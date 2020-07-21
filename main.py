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
		'-e', '--experiment',
		type = str,
		help = 'experiment name',
		required = True
	)
	parser.add_argument(
		'-f', '--format',
		type = str,
		help = 'target format',
		choices = ['tree', 'sequence'],
		default = 'sequence'
	)
	parser.add_argument(
		'-w', '--withhold', type=str,
		help='regex expressions matching substrings of lines which should be withheld from the train/test/val splits and placed in their own testing files', nargs='+')
	parser.add_argument(
		'-t', '--testing',
		type = str,
		help = 'regex expressions which match substrings of lines which should be placed only in the testing file',
		nargs = '+'
	)

	args = parser.parse_args()
	return args

def main():

	args = getArguments()

	print('Generating sentences from {0}.fcfg'.format(args.grammar))
	print('Writing to {0}.forms'.format(args.experiment))
	generate_forms.get_forms(args.grammar, args.experiment, args.format)
	print('Writing splits files')
	generate_forms.get_splits(
		{'train': 0.8, 'val': 0.10, 'test': 0.10},
		args.experiment,
		args.withhold,
		args.testing
	)

if __name__ == '__main__':
	main()