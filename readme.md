### To run:
`bash run.sh`

### Results
The script processes the test files using 1 to 5-grams and the following smoothing methods: witten_bell, absolute, katz, kneser_ney, presmoothed, unsmoothed.

It creates files stat-*n*.txt where *n* is the number of grams used.
Each file contains the outputs of the script conlleval.pl.

### Description of methods
#### Method 1
##### [best-F1]: 75.99 and kneser-nay (5-gram)
2 fst machines *with* additional features:
1. word -> lemma
2. lemma -> concept
Cost - log( c(concept) / c(total_concepts) ) for unk -> concept

#### Method 2
##### [best-F1] 76.42 and absolute (5-gram)
One single fst *with* additional features: word->lemma
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, lemma, tag, concept) / c (concept))

tested also with a prior probabilities when mapping unk to concept
the obtained result is 75.99

#### Method 3
One single fst *without* additional features: word->lemma
Cost 0 for unk -> concept
Cost word -> lemma - log(c(word, concept) / c (concept))

Best results:  76.37
witten_bell 2

Absolute 5:  76.15
Kneser-nay 5: ~76.15
