#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>


# This script can be used to download the likes of various people in a directory, 
# so you can create a model or simply analyze them later. It needs to get multiple 
# people at once because doing too many times the login on facebook you are 
# likely to be blocked.


from sys import argv
from os.path import isfile
import logging

from fbwrapper import fbwrapper



class LikesDownloader:	
	""" Download the likes for one or more persons """

	def __init__(self, username, password, download_dir, profiles, fb_obj=None, overwrite_likes=False):
		""" 
		If fb_obj is not None, it will be used instead of doing a new login.
		Profiles *must be* a list of nicknames, even if there is only one.
		"""
		self.__fb = fb_obj if fb_obj != None else fbwrapper.Facebook(username, password)
		self.__dir = download_dir
		self.__profiles = profiles
		self.__overwrite_likes = overwrite_likes
		
		self.__downloadLikes()
	
	
	def __downloadLikes(self):
		for profile in self.__profiles:
			if (self.__overwrite_likes and isfile(self.__dir + "/" + profile)):
				logging.warning("The profile '%s' has not been checked because it already exists" % profile)
			else:
				self.__write_likes(self.__fb.get_profile(profile).get_likes(), "%s/%s" % (self.__dir,  profile))
		

	def __write_likes(self, likes, fpath):
		""" Write the likes for one profile in a file """
		if len(likes) == 0:
			logging.warning("The file '%s' has not been written since it is empty" % fpath)
			return

		with open(fpath, "w") as f:	
			for like in likes:
				f.write(like + "\n")


if __name__ == "__main__":
	try:
		username, password, download_dir = argv[1:4]
		usernames = argv[4:]
	except ValueError:
		exit("Usage: download_likes.py username password download_dir url1...urlN")

	logging.getLogger().setLevel(logging.INFO)
	LikesDownloader(username, password, download_dir, usernames)

	
