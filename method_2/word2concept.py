import sys, os, math
from collections import Counter

"""
Compile:
# Define automata that maps word -> concept
python word2concept.py data/merged.txt word2concept.machine

where data/merged.txt is the merge between the two training files

# Compile automatas
fstcompile --isymbols=lexicon --osymbols=lexicon word2concept.machine > word2concept.fst
"""

train = sys.argv[1]
output = sys.argv[2]
wtlc = []

def removeDuplicate(l):
    return list(set(l))

def createAutomata(wordlemma, concept_costs):
    with open(output, 'w') as f:
        for word, concept, cost in wordlemma:
            f.write("0\t0\t" + word + "\t" + concept + "\t" + str(cost) +"\n")
        for cocost in concept_costs:
            concept, cost = cocost
#            f.write("0\t0\t<unk>\t" + concept + "\t" + str(cost) +"\n")
            f.write("0\t0\t<unk>\t" + concept + "\t0\n")
        f.write('0')
    
# read file
text1 = None
with open(train) as f:
    text1 = f.read()

lemmas = []
words = []
poss = []
concepts = []

# populate wordlemma
lines = text1.split("\n")
for line in lines:
    if not line.strip(): continue
    word, tag, lemma, concept = tuple(line.split("\t"))
    wtlc.append(word + "\t" + tag + "\t" + lemma + "\t" +concept)
    words.append(word)
    poss.append(tag)
    lemmas.append(lemma)
    concepts.append(concept)
    

# get weight
# p(tag | lemma) = c(word, tag, concept) / c(concept)
counter_wtlc = Counter(wtlc).most_common()
counter_lemmas = dict(Counter(lemmas))
counter_poss = dict(Counter(poss))
counter_words = dict(Counter(words))
counter_concepts = dict(Counter(concepts))

wordlemma = []
for wl in counter_wtlc:
    word_tag_lemma_concept, count = wl
    word, tag, lemma, concept = tuple(word_tag_lemma_concept.split("\t"))
    count_concept = counter_concepts[concept]
    prob = float(count) / float(count_concept)
    cost = - math.log(prob)
    cost = abs(cost)
    wordlemma.append((word, concept, cost))

# p(concept) = p(concept) / p (total_concepts)
concept_prob = []
number_of_concepts = len(concepts)
for concept in counter_concepts:
    count_concepts = counter_concepts[concept]
    prob = float(count_concepts) / float(number_of_concepts)
    cost = - math.log(prob)
    cost = abs(cost)
    concept_prob.append((concept, cost))
    
createAutomata(wordlemma, concept_prob)
