#!/bin/bash
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

cat $@ | sort | uniq -c | sort -r

