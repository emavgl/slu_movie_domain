# Mid-Term Project: FST and GRM Tools for SLU

## Report Abstract
This report investigates several configurations in developing a Generative Spoken Language Understanding Module (SLU)
given a dataset of conceptually-tagged utterances. The aim of the investigation is to compare results obtained with different
methods and parameter congurations in order to find which one performs better when evaluated over a given test set. From our
investigation, the best result in terms of Precision, Recall and F1 score is obtained by pre-processing the training set and us-
ing a composition between word2lemma FST and a language model with 9-gram and Kneser Ney smoothing algorithm.

For more information, please read the file *report.pdf*.

## How to run:
Each directory has a bash script called *run.sh* that executes all the
possible combination of n-grams and smoothing algorithm for that specific method.
method_1, method_2 and method_3 have also a run_best.sh script to executes the combination that gives the best F1 score.

The scripts processes the test files using 1 to 5-grams and the following smoothing methods: witten_bell, absolute, katz, kneser_ney, presmoothed, unsmoothed.

Scripts create files /method_*/stat/stat-*n*.txt where *n* is the number of grams used. Each file contains the outputs of the script conlleval.pl. If multiple smoothing algorithms are tested, the output will be appended in the same file.

To run all the run.sh scripts:
`bash run_all.sh`

To run all the run_best.sh scripts
`bash run_all_bests.sh`

### Methods
#### Baseline [best-F1]: 29.92
One single fst *without* additional features: word->lemma
and *without* compose it with the language model.

The costs are calculated as:
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, concept) / c (concept))

#### Method 1
##### [best-F1]: 75.25 and kneser-nay (5-gram)
2 fst machines *with* additional features:
1. word -> lemma
2. lemma -> concept

Cost for unk -> concept:
- log( c(concept) / c(total_concepts) )

#### Method 2
##### [best-F1] 76.42 and absolute (5-gram)
One single fst *with* additional features: word->lemma
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, lemma, tag, concept) / c (concept))

tested also with a prior probabilities when mapping unk to concept
the obtained result is 75.99

#### Method 3
##### [best-F1] 82.54 and kneser_ney (9-gram)
Method 2 + preprocessing of the training files.
preprocessing.py scripts appends the word to the O concepts.

One single fst *with* additional features: word->lemma
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, lemma, tag, concept) / c (concept))

#### Method 4
##### [best-F1] 82.76 and kneser_ney (9-gram)
Method 2 + preprocessing of the training files.
preprocessing.py script appends the word to the O concepts.

One single fst *without* additional features: word->lemma
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, concept) / c (concept))
