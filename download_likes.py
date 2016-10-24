#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


# Questo script può essere utilizzato per scaricare i 'mi piace' di varie persone 
# in una directory, per poi crearci un modello.


from sys import argv
import logging

from fbwrapper import fbwrapper



def write_likes(likes, fpath):
	if len(likes) == 0:
		logging.warning("Il file '%s' non è stato scritto poiché vuoto" % fpath)
		return

	f = open(fpath, "w")
	
	for like in likes:
		f.write(like + "\n")
	
	f.close()



try:
	username, password = argv[1:3]
except IndexError:
	exit("Uso: download_likes.py username password")	


logging.getLogger().setLevel(logging.INFO)
fb = fbwrapper.Facebook(username, password)

# Modificare, directory dove salvare i mi piace
PATHPR="/home/richard/Documents/pro/"


# Inserire qui le istruzioni per scaricare i mi piace
# Es
# write_likes(fb.get_profile("LINK").get_likes(), PATHPR + "nomefile")

print("Questo script deve essere modificato per funzionare, leggere il sorgente")

	