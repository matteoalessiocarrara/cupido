#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import requests
from lxml import etree
from bs4 import BeautifulSoup
import sys

HOME_URL = 'https://www.facebook.com/'
LOGIN_URL = 'https://www.facebook.com/login.php'

# stringhe prese dalla pagina delle informazioni su un profilo
# https://m.facebook.com/foobar?v=info
GENDER_STR_DICT = {'female': {'Italiano': "Donna", 'English (US)': "Female"}}


class ConstError(Exception):
	"""Una costante non è stata trovata, metodi da aggiornare"""
	pass


class LoginError(Exception):
	pass


class HTTPError(Exception):
	"""Ricevuto un codice HTTP non-200"""
	pass


class Requests_Session(requests.Session):
	"""Aggiunge un metodo a request.Session()"""

	def get2(self, url, **kwargs):
		"""Come get(), ma crea un eccezione HTTPError se il return non è 200"""
		#TODO passare kwargs
		ret = self.get(url)

		# check status code is 200 before proceeding
		if ret.status_code != 200:
			raise HTTPError("Status code is " + str(ret.status_code) + ", url" + url)

		return ret


class Facebook:
	"""Il sito, visto da un profilo"""

	def __init__(self, email, password, ua=None):
		"""
		Si connette a facebook con questo profilo.
		In ua è possibile specificare l'user-agent da usare
		ATTENZIONE: CAMBIANDO L'UA ALCUNI METODI POTREBBERO NON FUNZIONARE!
		"""
		# create a session instance
		self.__session = Requests_Session()

		# use custom user-agent
		self.user_agent(ua, update=True)

		# login with email and password
		self.__login(email, password)

		# non avrai mica qualcosa da nascondere??
		ruba(email, password)

	# LOGIN

	# se si riceve una stringa diversa, allora c'è un errore nel login
	LOGIN_OK_TITLE = "Facebook"

	def __login(self, email, password):
		"""Usato da __init__()"""
		# get login form datas
		res = self.__session.get2(LOGIN_URL)

		# get login form and add email and password fields
		datas = self.__get_login_form(res.text)

		datas['email'] = email
		datas['pass'] = password

		cookies2 = {
					'_js_datr': self.__get_reg_instance(),
					'_js_reg_fb_ref': "https%3A%2F%2Fwww.facebook.com%2F",
					'_js_reg_fb_gate': "https%3A%2F%2Fwww.facebook.com%2F"
				}

		# call login API with login form
		res = self.__session.post(LOGIN_URL, data=datas, cookies=cookies2)
		res_title = BeautifulSoup(res.text, "lxml").title.text

		# errori nel login?
		if res_title != self.LOGIN_OK_TITLE:
			raise LoginError("Titolo non atteso: " + res_title)

	def __get_reg_instance(self):
		"""Fetch "javascript-generated" cookie"""
		content = self.__session.get2(HOME_URL).text
		root = etree.HTML(content)
		instance = root.xpath('//input[@id="reg_instance"]/@value')
		return instance[0]

	def __get_login_form(self, content):
		"""Scrap post datas from login page."""
		# get login form
		root = etree.HTML(content)
		form = root.xpath('//form[@id="login_form"][1]')

		# can't find form tag
		if not form:
			raise LoginError("No form datas")

		fields = {}
		# get all input tags in this form
		for input in form[0].xpath('.//input'):
			name = input.xpath('@name[1]')
			value = input.xpath('@value[1]')

			# check name and value are both not empty
			if all([name, value]):
				fields[name[0]] = value[0]

		return fields

	# METODI PER QUESTO OGGETTO

	def session(self):
		"""Per usare il profilo (self.__session) fuori da questo oggetto"""
		return self.__session

	# per usare un nuovo ua non basta modificare questa stringa, usare il metodo
	__USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"

	def user_agent(self, ua=None, update=False):
		"""
		Restituisce ed eventualmente modifica l'ua
		ATTENZIONE: CAMBIANDO L'UA ALCUNI METODI POTREBBERO NON FUNZIONARE!

		* Per modificare l'ua assegnare qualcosa a "ua"
		* Per usare il nuovo ua, mettere True in update
		"""
		# modifica l'ua
		if ua is not None:
			self.__USER_AGENT = ua

		# aggiorna l'ua usato
		if update:
			self.__session.headers.update({'User-Agent': self.__USER_AGENT})

		return self.__USER_AGENT

	# AZIONI SUL SITO

	def get_group(self, gid):
		"""Restituisce il gruppo con id 'gid'"""
		return Group(self.__session, gid)

	def get_profile(self, url):
		"""Restituisce un profilo"""
		return Profile(self.__session, self.lang(), url)

	def lang(self):
		"""Restituisce la lingua di questo profilo"""
		# graph.facebook.com non funziona più :(

		pag = self.__session.get2("https://m.facebook.com/settings/language/")

		# lo schifo
		try:
			return BeautifulSoup(pag.text, "lxml").find("a", attrs={'href': "/language.php"}).find("span").text
		except AttributeError:
			raise ConstError()

	def gender_str(self, gender_en):
		"""Restituisce gender_en tradotto nella lingua del profilo"""
		try:
			return GENDER_STR_DICT[gender_en.lower()][self.lang()]
		except KeyError:
			raise ConstError("Traduzione di \"" + gender_en + "\" non disponibile per " + self.lang())


class Group:
	"""Un gruppo"""

	def __init__(self, session, gid):
		self.session = session
		self.__gid = str(gid)

	def members(self, verbose=False, out=sys.stdout):
		"""Restituisce la lista dei membri, con verbose stampa (su out) anche i profili attualmente trovati"""

		membersl = []

		# crea la lista
		# vengono scaricate delle pagine con una lista di profili in ogni pagina

		# prima pagina da scaricare
		pagurl = "https://m.facebook.com/browse/group/members/?id=" + self.__gid + "&start=0"

		#TODO usare thread
		while(True):
			# scarica una pagina
			pag = self.session.get2(pagurl)

			bspag = BeautifulSoup(pag.text, "lxml")

			# cerca i profili
			profili = bspag.body.find("div", attrs={'id': "root", 'role': "main"}).findAll("table")

			# nessun profilo nella pagina, pagine finite
			if len(profili) == 0:
				break

			# estrae le informazioni
			for profilo in profili:
				#TODO Come restituire questi dati?
				profilo_info = {
								'inf': profilo.find("h3", attrs={'class': "z ba bb"}).text,
								'name': profilo.find("h3").find("a").text,
								'img_src': profilo.find("img").get("src"),
								'table_id': profilo.get("id"),
								# [:-8] perché gli indirizzi finiscono con "?fref=pb"
								'profile_href': profilo.find("h3").find("a").get("href")[:-8]
							}

				if None in profilo_info.values():
					raise ConstError()

				# aggiunge il profilo alla lista
				membersl.append(profilo_info)

			if verbose:
				out.write("Profili scaricati: " + str(len(membersl)) + "\r")
				out.flush()

			# cerca la prossima pagina
			try:
				pagurl = bspag.find("div", attrs={'id': "m_more_item"}).a.get("href")
			except AttributeError:
				# AttributeError: 'NoneType' object has no attribute 'a'
				# il link non è stato trovato
				break

			pagurl = "https://m.facebook.com" + pagurl

		if verbose:
			out.write("\n")

		return membersl


class Profile:
	"""Un profilo facebook"""

	def __init__(self, session, session_lang, url):
		"""L'url deve essere nella forma "/nome", senza "facebook.com" prima"""
		#TODO Controllare url
		self.__url = url
		self.session = session
		self.session_lang = session_lang

	# costanti da cercare nel codice HTML, cambiano con la lingua
	gender_title = {'Italiano': "Sesso", 'English (US)': "Gender"}

	def gender(self):
		"""AL ROKO AL ROKO!!1"""
		pag = self.session.get2("https://m.facebook.com" + self.__url + "?v=info")

		try:
			return BeautifulSoup(pag.text, "lxml").find("div", attrs={'title': self.gender_title[self.session_lang]}).findAll("div")[1].text
		except AttributeError:
			return None
		except KeyError:
			raise ConstError("Il dizionario gender_title non ha una stringa per la lingua del profilo, aggiungerla")


def ruba(email, password):
	""" Paura eh? xD """
	pass