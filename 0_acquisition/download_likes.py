#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


# Questo script può essere utilizzato per scaricare i 'mi piace' di varie persone 
# in una directory, per poi crearci un modello o semplicemente analizzarle successivamente.
# È necessario scaricare più persone in una volta sola poiché facendo troppe volte
# il login su facebook si rischia di essere bloccati.


from sys import argv
import logging

from fbwrapper import fbwrapper



class LikesDownloader:

	def __init__(self, username, password, download_dir, profiles, fb_obj=None):
		"""Se fb_obj è diverso da None, verrà usato quello invece di fare un nuovo login"""
		self.__fb = fb_obj if fb_obj != None else fbwrapper.Facebook(username, password)
		self.__dir = download_dir
		self.__profiles = profiles
		
		self.__downloadLikes()
	
	
	def __downloadLikes(self):
		for profile in self.__profiles:
			self.__write_likes(self.__fb.get_profile(profile).get_likes(), "%s/%s" % (self.__dir,  profile))
		

	def __write_likes(self, likes, fpath):
		"""Scrive i 'mi piace' di un profilo in un file"""
		if len(likes) == 0:
			logging.warning("Il file '%s' non è stato scritto poiché vuoto" % fpath)
			return

		with open(fpath, "w") as f:	
			for like in likes:
				f.write(like + "\n")


if __name__ == "__main__":
	try:
		username, password, download_dir = argv[1:4]
		usernames = argv[4:]
	except ValueError:
		exit("Uso: download_likes.py username password download_dir url1...urlN")

	logging.getLogger().setLevel(logging.INFO)
	LikesDownloader(username, password, download_dir, usernames)

	