import sys, os

input = sys.argv[1]

text = None
with open(input) as f:
    text = f.read()

sentences = []
sentence = ""
for line in text.split("\n"):
    if not line.strip():
        sentences.append(sentence)
        sentence = ""
    else:
        concept = (line.split("\t"))[1]
        sentence = sentence + " " + concept

with open("concepts.txt", "w") as f:
    for s in sentences:
        f.write(s.strip() + "\n")
