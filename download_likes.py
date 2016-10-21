#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>

from sys import argv
import logging

from fbwrapper import fbwrapper


try:
	username, password, profile = argv[1:4]
except IndexError:
	exit("Uso: download_likes.py username password profile")	

logging.getLogger().setLevel(logging.INFO)
fb = fbwrapper.Facebook(username, password)

for like in fb.get_profile(profile).get_likes():
	print(like)
	