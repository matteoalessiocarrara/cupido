#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv, stdout
import csv
import logging

from libmodel import *

if len(argv) != 3:
	exit("Usage: model_diff.py model1.csv model2.csv")

logging.getLogger().setLevel(logging.DEBUG)
c = csv.writer(stdout)
likes = Model(csv=argv[1]) - Model(csv=argv[2])
for like in likes:
	# the number first and then the name because it is easier to split/sort
	c.writerow([likes[like], like])
