# Create lexicon
python createLexicon.py data/train1.txt data/train2_p.txt

# Define automata that maps word -> concept
python word2concept.py data/merged.txt word2concept.machine

# Compile automatas
fstcompile --isymbols=lexicon --osymbols=lexicon word2concept.machine > word2concept.fst

# Sort automatas in order to run fstcompose
fstarcsort word2concept.fst > word2concept_s.fst

## declare an array variable
#declare -a ngrams=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10")
declare -a ngrams=("7" "8" "9" "10")
#declare -a methods=("witten_bell" "absolute" "katz" "kneser_ney" "presmoothed" "unsmoothed")
declare -a methods=("presmoothed" "unsmoothed")

# Compile all training concepts
farcompilestrings --symbols=lexicon --unknown_symbol='<unk>' -keep_symbols=1 data/concepts.txt > concepts.far

# Compile all test sentences
farcompilestrings --unknown_symbol='<unk>' --symbols=lexicon -keep_symbols=1 data/sentences.txt > word_sentences.far

# Delete stats directory
rm -rf stats; mkdir stats;

## now loop through the above array
for i in "${ngrams[@]}"
do
    # Create Language Model
    ngramcount --order=$i --require_symbols=false concepts.far > concepts.cnts

    for m in "${methods[@]}"
    do
        ngrammake --method=$m concepts.cnts > trlm.lm

        # Delete old tmp files
        rm results.txt; rm -rf fst ; mkdir fst; cd fst; farextract --filename_suffix=.fst ../word_sentences.far; cd ..;

        # For each strings, process and put results into results.txt
        for f in ./fst/*
        do
            echo "Processing $f file using $i-gram and $m"
            fstcompose $f word2concept_s.fst | fstcompose - trlm.lm | fstrmepsilon | fstshortestpath | fsttopsort | fstprint --isymbols=lexicon --osymbols=lexicon  >> results.txt;
        done

        # Get processed concepts and prepare to_evaluate file
        awk '{print $4}' results.txt | paste -d '\t' data/NLSPARQL.test.data - | sed 's/\t/ /g' | sed -r 's/(O-(.)*)/O/' > to_evaluate.txt

        # Evaluate using conlleval
        perl conlleval.pl < to_evaluate.txt >> ./stats/stat_$i.txt
    done
done
