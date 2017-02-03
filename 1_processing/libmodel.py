#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

import csv


# TODO Anti-model, people weight


class Model(object):
	def __init__(self, csv=None, files=None):
		"""The model can be loaded from a previously created csv file, or created 
		from a list of files"""
		if csv != None:
			self.__load_from_csv(csv)
		elif files != None:
			self.__load_from_files(files)
		else:
			raise Exception("Uno dei parametri deve essere definito")


	def __load_from_csv(self, csvf):
		with open(csvf) as csvfile:
			reader = csv.reader(csvfile)
			self.__set_likes({rows[1]:float(rows[0]) for rows in reader})

	
	def __load_from_files(self, files):
		out = {}
		for lf in files:
			with open(lf) as f:
				for name in [l.strip('\n') for l in f.readlines()]:
					out[name] = out[name] + 1 if name in out.keys() else 1
		
		for key in out:
			out[key] = out[key]/float(len(files)) * 100
		
		self.__set_likes(out)

	
	def __set_likes(self, likes):
		self.__likes = likes

	
	def get_likes(self):
		return self.__likes

	
	def __sub__(self, other):
		"""other MUST BE an istance of this class"""
		tl = self.get_likes()
		ol = other.get_likes()
		rl = {}
		for key in set(list(tl.keys()) + list(ol.keys())):
				v = 0 + tl[key] if key in tl.keys() else 0
				v -= ol[key] if key in ol.keys() else 0
				rl[key] = v
				
		return rl

		
