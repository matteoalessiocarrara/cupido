#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


from sys import argv
import csv
import logging
import math


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
		model_likes_names.append(row["page"])
		model_likes_count.append(int(row["count"]))


rating = 0
with open(profile_likes_f) as pl:
	for like in pl.readlines():
		like = like.strip('\n')
		if like in model_likes_names:
			count = model_likes_count[model_likes_names.index(like)]
			
			if count >= math.floor(20./100 * models):
				logging.debug("Trovato like corrispondente: %s %s" % (count, like))
				rating += (1 * (count / float(models)))

print (rating, profile_likes_f)
		