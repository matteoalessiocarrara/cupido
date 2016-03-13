#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
#  Copyright 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import logging

import htmlfbapi


logging.basicConfig(level=logging.INFO)


username = raw_input("Username: ")
password = raw_input("Password: ")

# Questo è solo un test veloce, l'human emulation è una rottura di scatole
fb = htmlfbapi.Facebook(username, password, human_emulation_enabled=False)


your_gender = fb.my_profile.gender
your_gender_translations = your_gender.keys()

print "Tu sei:", your_gender
print "Questo genere può essere tradotto in queste lingue:", your_gender_translations


try:
	# Esempio di confronto che funziona indipendentemente dalla lingua del profilo
	# Anche se your_gender è stato recuperato in italiano, francese, o arabo, 
	# questo confronto funziona comunque, perché prima di confrontare traduce
	# nella stessa lingua (English (US))
	# TODO Non confrontare direttamente con una stringa, prendere la stringa da
	# get_gender_translations
	if your_gender['English (US)'] == "Female":
		print "Test ok"

except KeyError:
	print "Non c'è una traduzione in inglese per il genere del tuo profilo :/"


