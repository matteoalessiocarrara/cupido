#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# Input: files contenenti i mi piace di varie persone
# Output: conteggio dei mi piace in comune, ordine decrescente, csv 

python <<< "
import csv
import sys

c = csv.writer(sys.stdout)
for line in '''$(cat $@ | sort | uniq -c | sort -n -r)'''.split('\n'):
	l = line.strip()
	num = l.split(' ')[0]
	t = l[len(num) + 1:]
	c.writerow([t, num])
"



