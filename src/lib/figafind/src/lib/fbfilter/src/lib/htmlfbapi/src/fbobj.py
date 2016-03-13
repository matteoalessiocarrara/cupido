#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2015 - 2016 Matteo Alessio Carrara <sw.matteoac@gmail.com>
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

"""Oggetti di Facebook"""

from lib.fbwrapper.src import fbobj


# TODO Controllare versione libreria


class Profile(fbobj.Profile):

	# Struttura del dizionario: {'gender_en': {'lang': 'translation', ...}}
	get_gender_translations = {
								'female': {'Italiano': "Donna", 'English (US)': "Female"},
								'male': {'Italiano': "Uomo", 'English (US)': 'Male'}
								}


	def get_gender(self):
		# Tenere sincronizzata docstring con quella di fbobj.Profile.get_gender()
		"""
		Restituisce un dizionario con questa struttura:
		{lang: gender_str, lang: gender_str, ...}
		
		È sempre disponibile una chiave uguale alla lingua del profilo.
		La stringa del genere è "bho", quando non lo trova
		
		Eccezioni:
		
			KeyError
				Manca una costante per la lingua del profilo
		"""
		gender = super(Profile, self).get_gender()
		prof_lang = self.fb.my_profile.lang

		# XXX Generalizzare questa roba, servirà in altri metodi
		
		# Vediamo se ci sono delle traduzioni
		# Controlliamo ogni genere disponibile nel dizionario delle traduzioni
		for gender_en in self.get_gender_translations:

			this_gender = self.get_gender_translations[gender_en]
			
			# Se questo genere ha una traduzione anche nella lingua del profilo
			if this_gender.has_key(prof_lang):

				# Se il genere trovato è uguale a questo, restituisce il dizionario
				# di traduzioni
				if this_gender[prof_lang] == gender:
					return this_gender

		# Se siamo ancora qui, non ha trovato traduzioni
		# Restituiamo un dizionario con il genere solo nella lingua del profilo
		return {prof_lang: gender}

	gender = property(get_gender)
