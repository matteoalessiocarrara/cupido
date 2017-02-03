#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# Remove the duplicate likes in each file of a directory


if [[ $# -ne 1 ]]; then
	echo "Usage: sanitize_likes.sh directory_with_like_files"
	exit 1
fi

TMPDIR=/tmp/$(echo $1 | md5sum | cut -d ' ' -f1)
mkdir $TMPDIR

for file in $(ls $1)
do
	# We cant write the output directly in the input file, since the shell reset
	# it before executing the comand
	cat "$1/$file" | sort | uniq -u > "$TMPDIR/$file"
	mv "$TMPDIR/$file" "$1/$file"
done

rm -rf $TMPDIR
