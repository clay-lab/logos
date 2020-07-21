# logos (λόγος)

`logos` is a family of experiments designed to explore the acquisition of 
semantic representations of natural-language sentences by neural networks. It 
uses @clay-lab's `transductions` library to train Seq2Seq models on datasets 
and analyze the results.

`logos` uses Featural Context-Free Grammars from `nltk` to produce training
data consisting of input sentences, a transformation token `sem`, and target
outputs of predicate logic. `transductions` models may then be trained on these
datasets.

The `experiments` directory contains the trained models and logs for several
different experiments run with `logos` datasets:

* **Alice-\*:** The Alice-\* family of experiments explore the ability of 
Seq2Seq networks to generalize knowldge of anaphors (reflexive pronouns) to 
novel antecedents. The training data consists of transitive sentences of the form `PERSON-1 VERBS {PERSON-2, him/herself}`, where `PERSON-1` and `PERSON-2` may be distinct, and intransitive sentences of the form `PERSON VERBS`. In each experiment, certain reflexive combinations are withheld from the training data and we test the networks' abilities to generalize to these new antecedents.
