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

"""Oggetti secondari"""

from bs4 import BeautifulSoup

import myexceptions
import logging

# configurazione del sistema di logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class GenericFBObj(object):
	"""Un generico oggetto su Facebook"""

	def  __init__(self, fbobj):
		"""
		Parametri:
		* fbobj: un oggetto Facebook
		"""
		self.fbobj = fbobj

	def get_fbobj(self):
		"""Restituisce l'oggetto Facebook utilizzato in questo oggetto"""
		return self.__fbobj

	def  set_fbobj(self, fbobj):
		"""Cambia l'oggetto Facebook usato in questo oggetto"""
		self.__fbobj = fbobj

	def get_fbobj_session(self):
		"""Restituisce la sessione dell'oggetto Facebook"""
		return self.fbobj.get_session()

	fbobj = property(get_fbobj, set_fbobj)
	session = property(get_fbobj_session)


# HACK Usare la classe str, questa dovrebbe essere una stringa!
class FBLang(GenericFBObj):
	"""
	La "stringa" che rappresenta la lingua di un profilo
	ATTENZIONE: Questo oggetto NON È UN OGGETTO str, per ottenere la stringa usare str()
	"""

	def __init__(self, fbobj, use_cache=False):
		"""
		Parametri:
		* fbobj deve essere un oggetto Facebook
		* con use_cache si può attivare o disattivare la cache della lingua
		"""
		super(FBLang, self).__init__(fbobj)
		# La cache potrebbe anche essere attiva, chi modifica la lingua del profilo
		# da un momento all'altro?
		# Io non l'ho più modificata dalla creazione del profilo
		# Ma comunque per evitare malfunzionamenti non usiamo la cache di default
		self.cache_status = use_cache

	def __str__(self):
		"""
		Restituisce la stringa con la lingua del profilo
		Utilizza automaticamente la cache se è attiva
		"""
		if self.cache_status == True:
			return self.cached_lang
		else:
			return self.server_lang

	def update_cache(self):
		"""
		Aggiorna la cache della lingua
		Restituisce False se la cache non è attiva
		"""
		if self.cache_status == True:
			logger.debug("Updating lang cache")
			self.__set_cached_lang(self.server_lang)
			return True
		else:
			logger.warning("FBLang.update_cache(): Cache is not active")
			return False

	def get_cached_lang(self):
		"""Restituisce la lingua memorizzata nella cache, se la cache non è
		attiva restituisce str(None)"""
		if self.cache_status == True:
			return self.__cached_lang
		else:
			logger.warning("FBLang.get_cached_lang(): Cache is not active")
			return str(None)

	def __set_cached_lang(self, lang):
		self.__cached_lang = lang

	def get_cache_status(self):
		"""Restituisce True se la cache è attiva, False se non è attiva"""
		return self.__use_lang_cache

	def set_cache_status(self, use_cache):
		"""
		Attiva o disattiva la cache per la lingua

		Quando attiva, la lingua viene scaricata una sola volta e conservata
		in una varibaile
		Quando non attiva, ogni volta che è richiesta viene riscaricata

		Se si usa la cache e la lingua viene modificata sul sito, la cache deve
		essere aggiornata con self.update_cache()
		Altrimenti alcuni metodi smetteranno di funzionare

		Parametri:
		 * use_cache: deve contenere o True o False
		"""
		self.__use_lang_cache = bool(use_cache)
		logger.debug("use_cache = %s" % use_cache)

		if use_cache:
			self.update_cache()

	def get_server_lang(self):
		"""Restituisce la lingua del profilo scaricandola da Facebook"""

		logger.debug("Downloading language")
		# graph.facebook.com non funziona più :(
		pag = self.session.get2("https://m.facebook.com/settings/language/")

		try:
			b = BeautifulSoup(pag.text, "lxml")
			return b.find("a", attrs={'href': "/language.php"}).find("span").text
		except AttributeError:
			err = "Impossibile ottenere la lingua del profilo! Metodo da aggiornare"
			logger.critical(err)
			raise myexceptions.ConstError(err)

	cached_lang = property(get_cached_lang)
	cache_status = property(get_cache_status, set_cache_status)
	server_lang = property(get_server_lang)
