import sys, os, math
from collections import Counter

train1 = sys.argv[1]
output = sys.argv[2]
wordlemma_strings = []

def removeDuplicate(l):
    return list(set(l))

def createAutomata(wordlemma, lems):
    with open(output, 'w') as f:
        for word, lemma, cost in wordlemma:
            f.write('0\t0\t' + word + "\t" + lemma + "\t" + str(cost) +"\n")
        for lemma in lems:
            f.write('0\t0\t' + lemma + "\t" + lemma + "\t" + str(0) +"\n")
        f.write("0\t0\t<unk>\t<unk>\t0\n")
        f.write('0')
    
# read file
text1 = None
with open(train1) as f:
    text1 = f.read()

lemmas = []
words = []

# populate wordlemma
lines = text1.split("\n")
for line in lines:
    if not line: continue
    pieces = line.split("\t")
    wordlemma_strings.append(pieces[0] + "\t" + pieces[2])
    lemmas.append(pieces[2])
    words.append(pieces[0])
    

# get weight
# count(word, lemma) / count(lemma)
counter_wordslemma = Counter(wordlemma_strings).most_common()
counter_lemmas = dict(Counter(lemmas))
counter_words = dict(Counter(words))

wordlemma = []
for wl in counter_wordslemma:
    word_lemma, count = wl
    word, lemma = tuple(word_lemma.split("\t"))
    count_lemma = counter_lemmas[lemma]
    count_word = counter_words[word]
    prob = float(count) / float(count_lemma)
    cost = - math.log(prob)
    cost = abs(cost)
    wordlemma.append((word, lemma, cost))
 
uniqueWords = list(set(words))
lemmasToAdd = [lemma for lemma in lemmas if lemma not in uniqueWords]
createAutomata(wordlemma, sorted(list(set(lemmasToAdd))))
