# Create lexicon
python createLexicon.py data/train1.txt data/train2.txt

# Define automata that maps word -> concept
python word2concept.py data/merged.txt word2concept.machine

# Compile automatas
fstcompile --isymbols=lexicon --osymbols=lexicon word2concept.machine > word2concept.fst

# Sort automatas in order to run fstcompose
fstarcsort word2concept.fst > word2concept_s.fst

# Compile all training concepts
farcompilestrings --symbols=lexicon --unknown_symbol='<unk>' -keep_symbols=1 data/concepts.txt > concepts.far

# Compile all test sentences
farcompilestrings --unknown_symbol='<unk>' --symbols=lexicon -keep_symbols=1 data/sentences.txt > word_sentences.far

# Delete old tmp files
rm -rf stats; rm results.txt; rm -rf fst ;
mkdir stats; mkdir fst; cd fst; 

farextract --filename_suffix=.fst ../word_sentences.far; cd ..;

# For each strings, process and put results into results.txt
for f in ./fst/*
do
    echo "Processing $f file"
    fstcompose $f word2concept_s.fst | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=lexicon --osymbols=lexicon  >> results.txt;
done

# Get processed concepts and prepare to_evaluate file
awk '{print $4}' results.txt | paste -d '\t' data/NLSPARQL.test.data - > to_evaluate.txt

# Evaluate using conlleval
perl conlleval.pl -d "\t" < to_evaluate.txt > ./stats/stat_best.txt
