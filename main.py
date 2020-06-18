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
		'-t', '--task',
		type = str,
		help = 'task name',
		required = True
	)

	args = parser.parse_args()
	return args

def main():

	args = getArguments()

	print('Generating sentences from {0}'.format(args.grammar))
	generate_forms.get_forms(args.grammar, args.task)
	print('Writing splits files')
	generate_forms.get_splits(
		{'train': 0.8, 'val': 0.10, 'test': 0.10},
		args.task
	)

if __name__ == '__main__':
	main()