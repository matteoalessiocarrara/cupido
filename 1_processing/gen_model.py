#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv, stdout
import csv
import logging


def calc_likes_percent(files):
	out = dict()
	for lf in files:
		with open(lf) as f:
			for name in [l.strip('\n') for l in f.readlines()]:
				out[name] = out[name] + 1 if name in out.keys() else 1
	
	for key in out:
		out[key] = out[key]/float(len(files)) * 100
	
	return out


def main():
	if ("-m" in argv) and ("-a" in argv):
		model_likes_files = argv[argv.index("-m") + 1 : argv.index("-a")]
		anti_likes_files = argv[argv.index("-a") + 1:]
	else:
		exit("Uso: -m likes1..likesN -a likes1..likesN")
	
	if len(model_likes_files) != len(anti_likes_files):
		logging.warning("I modelli non sono in numero uguale")
		
	if (len(model_likes_files) == 0) or (len(anti_likes_files) == 0):
		logging.warning("Mancano i file per un modello")

	c = csv.writer(stdout)
	model_likes_percent = calc_likes_percent(model_likes_files)
	anti_likes_percent = calc_likes_percent(anti_likes_files)
	for key in model_likes_percent:
			c.writerow([(model_likes_percent[key] - anti_likes_percent[key] if key in anti_likes_percent.keys() else model_likes_percent[key]), key])


logging.getLogger().setLevel(logging.DEBUG)
main()
