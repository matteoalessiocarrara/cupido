#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv, stdout
import csv
import logging

from libmodel import *


if len(argv) < 2:
	exit("Usage: gen_model.py file1...fileN")

logging.getLogger().setLevel(logging.DEBUG)
c = csv.writer(stdout)
likes = Model(files=argv[1:]).get_likes()
for like in likes:
	# the number first and then the name because it is easier to split/sort
	c.writerow([likes[like], like])
	
