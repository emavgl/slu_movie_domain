import sys, os

input = sys.argv[1]

text = None
with open(input) as f:
    text = f.read()

sentences = []
sentence = ""
for line in text.split("\n"):
    if not line:
        sentences.append(sentence)
        sentence = ""
    else:
        word = (line.split("\t"))[0]
        sentence = sentence + " " + word

with open("sentences.txt", "w") as f:
    for s in sentences:
        f.write(s.strip() + "\n")
