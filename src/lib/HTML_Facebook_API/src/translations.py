#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2015 Matteo Alessio Carrara <sw.matteoac@gmail.com>
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

"""Funzioni e oggetti per la gestione di stringhe dipendenti dalla lingua"""

import myexceptions
import logging

# configurazione del sistema di logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Roba per la stringa del sesso

class GendersDict(dict):
	"""Dizionario con metodi specifici"""

	def __init__(self, dict_):
		"""
		Struttura del dizionario: dizionario[gender_en_str][facebook_lang_str]
		"""
		super(GendersDict, self).__init__(dict_)
		# TODO Controllare se formato dizionario corretto

	def get_genders(self):
		"""Lista dei generi disponibili nel dizionario"""
		return self.keys()

	def translations(self, gender):
		"""Restituisce le traduzioni disponibili per un genere"""
		try:
			return self[gender].keys()
		except KeyError:
			err = "\"%s\"  non è nel dizionario" % gender
			logger.error("GendersDict.translations(): %s", err)
			raise KeyError(err)

	genders = property(get_genders)

# traduzioni per la stringa del sesso, dizionario normale
# traduzioni ricavate dalla pagina delle informazioni su un profilo:
# https://m.facebook.com/foobar?v=info
# stringhe della lingua estratte da:
# https://m.facebook.com/settings/language/
# struttura del dizionario: dizionario[gender_en_str][facebook_lang_str]
# ATTENZIONE: dizionario attualmente incompleto, aggiungere le traduzioni necessarie
GENDER_STR_NDICT = {'female': {'Italiano': "Donna", 'English (US)': "Female"}}

# traduzioni per la stringa del sesso, oggetto GendersDict
# ci sono dei metodi per rendere più semplice l'uso del dizionario
GENDER_STR_DICT = GendersDict(GENDER_STR_NDICT)

def translate_gender(gender_en, translate_lang):
	"""Wrapper per GENDER_STR_DICT, con eccezioni più dettagliate"""

	gender_en = gender_en.lower()

	if not (gender_en in GENDER_STR_DICT.genders):
		err = "Gender \"%s\" non è nel dizionario" % gender_en
		logger.error(err)
		raise KeyError(err)

	if not (translate_lang in GENDER_STR_DICT.translations(gender_en)):
		err = "Traduzione per la lingua \"%s\" non trovata" % translate_lang
		logger.error("translate_gender(): %s", err)
		raise KeyError(err)

	ret = GENDER_STR_DICT[gender_en][translate_lang]
	logger.debug("Translated, %s = %s", gender_en, ret)
	return ret
