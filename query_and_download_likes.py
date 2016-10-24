#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

# Questo script esegue una ricerca su facebook, e scarica i 'mi piace' per le prime
# N persone dei risultati

from sys import argv
import logging

from fbwrapper import fbwrapper

from download_likes import LikesDownloader


try:
	username, password, download_dir, query = argv[1:5]
except ValueError:
	exit("Uso: download_likes.py username password download_dir query [max_items]")

max_items = None if len(argv) < 6 else int(argv[5])


logging.getLogger().setLevel(logging.INFO)
fb = fbwrapper.Facebook(username, password)

usernames = []
for person in fb.people_search(query, max_items):
	usernames.append(person["url"].split("/")[3].split("?")[0])

LikesDownloader(None, None, download_dir, usernames, fb)