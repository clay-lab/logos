# logos
Translating sentences into logical forms

## Instructions
`logos` generates a TSV file of sentences and their logical forms as specified by the provided Featural Context-Free Grammar (FCFG). To generate the file for the provided FCFG, run `logos` as follows from the terminal.
```bash
$ python3 main.py
```
This will produce a TSV file named `forms.txt` whose contents is formatted as follows.
```
Example sentence \t Logical form
```

`logos` takes the following command-line arguments:
```
-g, --grammar: file containing grammar (FCFG) to generate logical forms
-o, --output: output file
```

### Unit Testing
In order to generate nice, parsable output, `logos` overrides the formatting of
several `nltk` classes. This is somewhat brittle, and as new forms of output 
are added it is best to add unit tests for the new cases. To test a module,
run the following command in the terminal:
```bash
# Testing file MODULE.py
$ python3 -m unittest test_MODULE
```
