import sys, os, math
from collections import Counter

train = sys.argv[1]
output = sys.argv[2]
lemmaposconcept_strings = []

def removeDuplicate(l):
    return list(set(l))

def createAutomata(wordlemma, concept_costs):
    with open(output, 'w') as f:
        for lemma, concept, cost in wordlemma:
            f.write("0\t0\t" + lemma + "\t" + concept + "\t" + str(cost) +"\n")
        for cocost in concept_costs:
            concept, cost = cocost       
            f.write("0\t0\t<unk>\t" + concept + "\t" + str(cost) +"\n")
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
    lemmaposconcept_strings.append(lemma + "\t" + tag + "\t" + concept)
    words.append(word)
    poss.append(tag)
    lemmas.append(lemma)
    concepts.append(concept)
    

# get weight
# p(tag | lemma) = c(lemma, tag, concept) / c(concept)
counter_lemmaposconcept = Counter(lemmaposconcept_strings).most_common()
counter_lemmas = dict(Counter(lemmas))
counter_poss = dict(Counter(poss))
counter_words = dict(Counter(words))
counter_concepts = dict(Counter(concepts))

wordlemma = []
for wl in counter_lemmaposconcept:
    lemma_tag_concepts, count = wl
    lemma, tag, concept = tuple(lemma_tag_concepts.split("\t"))
    count_concepts = counter_concepts[concept]
    prob = float(count) / float(count_concepts)
    cost = - math.log(prob)
    cost = abs(cost)
    wordlemma.append((lemma, concept, cost))

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
