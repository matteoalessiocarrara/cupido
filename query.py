#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# Questo script esegue solo una ricerca su facebook, e restituisce le persone trovate.
# I mi piace potranno essere scaricati successivamente con l'altro script

from sys import argv
import logging

from fbwrapper import fbwrapper


try:
	username, password, query = argv[1:4]
except ValueError:
	exit("Uso: query.py username password query [max_items]")

max_items = None if len(argv) < 5 else int(argv[4])


logging.getLogger().setLevel(logging.INFO)
fb = fbwrapper.Facebook(username, password)

for person in fb.people_search(query, max_items):
	print("%s %s" % (fbwrapper.Profile.nick_from_url(person["url"]), person["name"]))
