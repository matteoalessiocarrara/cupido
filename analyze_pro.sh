#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

python <<< "
for line in '''$(cat $@ | sort | uniq -c | sort -n -r)'''.split('\n'):
	l = line.strip()
	num = l.split(' ')[0]
	t = l[len(num) + 1:]
	print ('\"%s\", %s' % (t, num))
"



