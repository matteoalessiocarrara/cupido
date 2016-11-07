#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

if [[ -z $1 ]]; then
	echo "Passare il nome del file"
	exit 1
fi

cat $1 | sort -n -r -k1 -t,
