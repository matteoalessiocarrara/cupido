#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


from sys import argv
import csv
import logging
import math

# Quante volte deve essere ripetuto un 'mi piace' nel modello per essere considerato
MIN_LIKE_PERCENT = 20

try:
	profile_likes_f, model_likes_f, models = argv[1:4]
	models = int(models)
except ValueError:
	exit("Uso: rate.py profile_likes model_likes models")

logging.getLogger().setLevel(logging.INFO)


model_likes_names = []
model_likes_count = []
with open(model_likes_f) as f:
	for row in csv.DictReader(f, fieldnames=["page", "count"]):
		if int(row["count"]) >= math.floor(MIN_LIKE_PERCENT/100. * models):
			model_likes_names.append(row["page"])
			model_likes_count.append(int(row["count"]))

matching = 0
goodness = 0
rating = 0
with open(profile_likes_f) as pl:
	for like in pl.readlines():
		like = like.strip('\n')
		if like in model_likes_names:
			matching += 1
			goodness += model_likes_count[model_likes_names.index(like)]
	
	pl.seek(0, 0)
	rating = (float(matching) / len(pl.readlines()) * float(goodness) / sum(model_likes_count)) * 100
	print (rating, profile_likes_f)
		