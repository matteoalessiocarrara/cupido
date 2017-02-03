#!/bin/bash
# Copyright 2016 - 2017 Matteo Alessio Carrara <sw.matteoac@gmail.com>


if [[ $# -ne 2 ]]; then
	echo "Usage: directory_with_people_to_be_evaluated csv_model"
	exit 1
fi

PR_DIR=$1
CSV_MODEL=$2

for p in $(ls $PR_DIR); do
	python rate.py $PR_DIR/$p $CSV_MODEL
done
