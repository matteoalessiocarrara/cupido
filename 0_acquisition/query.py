#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# This script only performs a search on facebook, and returns the people found. 
# The likes can be downloaded later with the other script.

from sys import argv
import logging

from fbwrapper import fbwrapper


try:
	username, password, query = argv[1:4]
except ValueError:
	exit("Usage: query.py username password query [max_items]")

max_items = None if len(argv) < 5 else int(argv[4])


logging.getLogger().setLevel(logging.INFO)
fb = fbwrapper.Facebook(username, password)

for person in fb.people_search(query, max_items):
	print("%s %s" % (fbwrapper.Profile.nick_from_url(person["url"]), person["name"]))
