#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


from sys import argv
import csv
import logging
import math

try:
	profile_likes_f, model_likes_f = argv[1:3]
except ValueError:
	exit("Uso: rate.py profile_likes model_likes")

logging.getLogger().setLevel(logging.INFO)


model_likes_names = []
model_likes_value = []
with open(model_likes_f) as f:
	for row in csv.DictReader(f, fieldnames=["value", "page"]):
		model_likes_names.append(row["page"])
		model_likes_value.append(float(row["value"]))

matching = 0
goodness = 0
with open(profile_likes_f) as pl:
	for like in [l.strip('\n') for l in pl.readlines()]:
		if like in model_likes_names:
			matching += 1
			goodness += model_likes_value[model_likes_names.index(like)]
	
	pl.seek(0, 0)
	rating = float(matching) / len(pl.readlines()) * float(goodness) / matching
	print (rating, profile_likes_f)
		
