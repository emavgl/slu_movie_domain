import os, sys
from collections import Counter

"""
Usage: python preprocessing.py data/train2.txt 
The script append the word to the O concepts
"""

file2 = sys.argv[1]

text2 = None
with open(file2) as f:
    text2 = f.read()

lines = text2.split("\n")
output_lines = []
for line in lines:
    if not line:
	output_lines.append(line)
	continue
    pieces = line.split("\t")
    co = pieces[1]
    if co == 'O':
        pieces[1] = 'O-'+pieces[0]
    output_lines.append('\t'.join(pieces))

# write into file
counter = 1
with open('train2_p.txt', 'w') as f:
    for i, line in enumerate(output_lines):
	if i > 0: f.write("\n")	
	new = line.replace('\n', '') # remove \n if exists
        f.write(new)

