import os, sys
from collections import Counter

"""
Usage: python createLexicon.py data/train1.txt data/train2.txt 
From the first one, it takes: word, tag and lemma
From the second one, it takes: context

The script puts them all together and create a file called "lexicon"
"""

def removeDuplicates(l):
    return sorted(list(set(l)))

file1 = sys.argv[1]
file2 = sys.argv[2]

words = []
tags = []
lemmas = []
contexts = []

# read file
text1 = None
with open(file1) as f:
    text1 = f.read()

text2 = None
with open(file2) as f:
    text2 = f.read()

# populate lists words and tags with repetition
lines = text1.split("\n")
for line in lines:
    if not line: continue
    pieces = line.split("\t")
    word = pieces[0]
    tag = pieces[1]
    lemma = pieces[2]
    words.append(word)
    tags.append(tag)
    lemmas.append(lemma)

lines = text2.split("\n")
for line in lines:
    if not line: continue
    pieces = line.split("\t")
    co = pieces[1]
    contexts.append(co)

# [smoothing] remove words that appear only one time
# counter = Counter(words).most_common() + 
# filtered_words = [w for w, c in counter if c > 1]

# concat sorted words and tags into a single list "words"
li = words + lemmas + contexts + tags
toinsert = removeDuplicates(li)

# write into file
counter = 1
with open('lexicon', 'w') as f:
    f.write('<eps>\t0\n')
    for word in toinsert:
        f.write(word + "\t" + str(counter) + "\n")
        counter = counter + 1
    f.write('<unk>\t' + str(counter))
