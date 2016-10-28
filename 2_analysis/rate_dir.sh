#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


if [[ $# -ne 3 ]]; then
	echo "Uso: directory_confrontare modello_csv membri_csv"
	exit 1
fi

PR_DIR=$1
CSV_MODEL=$2
CSV_MEMBERS=$3

for p in $(ls $PR_DIR); do
	python rate.py $PR_DIR/$p $CSV_MODEL $CSV_MEMBERS
done
