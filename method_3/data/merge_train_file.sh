awk '{print $2}' train2_p.txt > train2_col.txt
paste -d "\t" train1.txt train2_col.txt > merged.txt

