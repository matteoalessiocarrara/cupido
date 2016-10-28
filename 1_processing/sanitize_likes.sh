#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# Rimuove i like duplicati in ogni profilo di una directory


if [[ $# -ne 1 ]]; then
	echo "Passare la directory con i mi piace"
	exit 1
fi

TMPDIR=/tmp/$(echo $1 | md5sum | cut -d ' ' -f1)
mkdir $TMPDIR

for file in $(ls $1)
do
	cat "$1/$file" | sort | uniq -u > "$TMPDIR/$file"
	mv "$TMPDIR/$file" "$1/$file"
done

rm -rf $TMPDIR
