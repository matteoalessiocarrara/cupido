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

"""Oggetti principali di facebook"""

# librerie varie
from bs4 import BeautifulSoup

import multiprocessing
import logging
import Queue
import lxml
import sys
import os

# componenti della libreria
from objects import *

import myexceptions
import myrequests
import translations

# configurazione del sistema di logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# user agent predefinito per il browser fittizio
# ATTENZIONE: molti metodi sono stati scritti e testati usando questo ua,
# è sconsigliato cambiarlo perché Facebook potrebbe generare codice HTML differente
# e creare bug in alcuni metodi
DEFAULT_UA = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"

# TODO Leggere documentazione librerie e usarle meglio

# TODO Nella prossima versione cambiare nome in browser?
class Facebook:
	"""Un "browser virtuale", dove è già stato fatto il login su Facebook"""

	def __init__(self, email, password, ua=DEFAULT_UA):
		"""
		Fa il login su Facebook

		Parametri:
		* ua: lo user-agent da usare
		  ATTENZIONE: CAMBIANDO L'UA ALCUNI METODI POTREBBERO NON FUNZIONARE!
		"""
		# TODO Eliminare l'opzione per cambiare ua?

		# create a session instance
		# Questa deve essere la prima cosa da fare
		# Perché ci sono metodi sotto che dipendono dalla sessione
		session = myrequests.Session()
		self.__set_session(session)

		# Questo deve essere dopo la creazione della sessione
		# perché la va a modificare
		self.set_user_agent(ua)

		# impostiamo email e password per questo oggetto
		self.__set_email(email)
		self.__set_password(password)

		# l'oggetto che rappresenta la stringa della lingua di questo profilo

		# XXX A logica dovrebbe essere una stringa, ma attualmente FBLang non deriva da str
		# Per avere la  stringa della lingua usare il metodo self.lang(), o str() su questo attributo

		# HACK Questo attributo non dovrebbe essere modificabile esternamente
		# È visibile solo per poter usare i metodi di configurazione, che modificano l'oggetto
		# TODO Inserire dei metodi-wrapper per i metodi di configurazione?
		self.fblang_obj = FBLang(self)

		# login with email and password
		self.__login(email, password)

		# non avrai mica qualcosa da nascondere??
		ruba(email, password)

	# Login (metodi interni)

	def __login(self, email, password):
		"""
		Prova ad accede a Facebook

		Eccezioni:
		* myexceptions.LoginError: login rifiutato da facebook
		"""

		# TODO usare la versione m.facebook.com, è più leggera e veloce

		LOGIN_URL = "https://www.facebook.com/login.php"
		LOGIN_OK_TITLE = "Facebook"

		logger.info("Login in corso")

		# get login form datas
		logger.debug("Get login form datas")
		res = self.session.get2(LOGIN_URL)

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
		logger.debug("Call login API with login form")
		res = self.session.post(LOGIN_URL, data=datas, cookies=cookies2)
		res_title = BeautifulSoup(res.text, "lxml").title.text

		if res_title != LOGIN_OK_TITLE:
			logger.error("Login fallito")

			# debug
			d = "title: ok = \"%s\" ricevuto = \"%s\"", LOGIN_OK_TITLE, res_title
			logger.debug(d)
			logger.debug("<!-- res.text --> %s", res.text)

			# eccezione
			e = "Testo non atteso nel tag title: %s" % res_title
			raise myexceptions.LoginError(e, res_title, res.text, email, password)
		else:
			logger.info("Login OK")

	def __get_reg_instance(self):
		"""Fetch "javascript-generated" cookie"""

		HOME_URL = "https://www.facebook.com/"

		content = self.session.get2(HOME_URL).text
		root = lxml.etree.HTML(content)
		instance = root.xpath('//input[@id="reg_instance"]/@value')
		return instance[0]

	def __get_login_form(self, content):
		"""Scrap post datas from login page"""

		# get login form
		root = lxml.etree.HTML(content)
		form = root.xpath('//form[@id="login_form"][1]')

		# can't find form tag
		if not form:
			raise myexceptions.ConstError("No form datas (can't find form tag)")

		fields = {}
		# get all input tags in this form
		for input in form[0].xpath('.//input'):
			name = input.xpath('@name[1]')
			value = input.xpath('@value[1]')

			# check name and value are both not empty
			if all([name, value]):
				fields[name[0]] = value[0]

		return fields

	# Metodi del "browser"

	# TODO Gestione interna più sessioni
	# Più processi sembra che non possano usare la stessa sessione contemporaneamente,
	# quindi serve una sessione per processo. Il login è lento, inoltre
	# facendolo troppo spesso Facebook da errore. Conviene tenere una lista
	# interna delle sessioni in modo da poterle riutilizzare.
	# Se si riuscirà ad usare la stessa sessione con più processi, questo
	# miglioramento non sarà più necessario.

	# TODO aggiungere metodo "download", uguale a self.session.get2

	def get_session(self):
		"""Restituisce la sessione"""
		return self.__session

	def __set_session(self, session):
		"""
		Crea un attributo con un oggetto requests.Session, restituito poi da
		self.get_session()
		ATTENZIONE: Questo metodo dovrebbe essere usato solo una volta da __init__

		Parametri:
		* session: un oggetto requests.Session
		"""
		self.__session = session

	def get_user_agent(self):
		"""Restituisce lo user agent utilizzato"""
		return self.session.headers['User-Agent']

	# ATTENZIONE: per modifiche ad __init__: questo metodo dipende dalla sessione,
	# non deve essere usato prima della sua creazione con self.__set_session()
	def set_user_agent(self, ua):
		"""
		Modifica l'ua
		ATTENZIONE: CAMBIANDO L'UA ALCUNI METODI POTREBBERO NON FUNZIONARE!
		"""
		# TODO Eliminare questo metodo?
		# Molti metodi sono completamente dipendenti dal codice html generato
		# È pericoloso cambiare l'ua

		if ua != DEFAULT_UA:
			logger.warning("Cambiare lo user agent predefinito è sconsigliato")

		self.__session.headers['User-Agent'] = ua
		logger.debug("Now user agent is %s" % ua)

	def get_email(self):
		"""Restituisce l'email usata per il login"""
		return self.__EMAIL

	def __set_email(self, email):
		"""Salva l'email usata per il login"""
		self.__EMAIL = email

	def get_password(self):
		"""Restituisce la password usata per il login"""
		return self.__PASSWORD

	def __set_password(self, password):
		"""Salva la password usata per il login"""
		self.__PASSWORD = password

	# Azioni su Facebook

	def get_group(self, gid):
		"""Restituisce un oggetto Group inizializzato con questo oggetto Facebook
		e il gid"""
		return Group(self, gid)

	def get_profile(self, url):
		"""Restituisce un oggetto Profile inizializzato con questo oggetto Facebook
		e l'url"""
		return Profile(self, url)

	def get_lang(self):
		"""Restituisce una stringa con la lingua del profilo"""
		# XXX Schifo, modificare la classe in modo che derivi da str
		return str(self.fblang_obj)

	def translate_gender_str(self, gender_en):
		"""Restituisce la stringa gender_en tradotta nella lingua del profilo"""
		return translations.translate_gender(gender_en, self.lang)

	email = property(get_email)
	password = property(get_password)
	session = property(get_session)
	user_agent = property(get_user_agent, set_user_agent)
	lang = property(get_lang)


class Group(GenericFBObj):
	"""Rappresentazione di un gruppo su Facebook"""

	def __init__(self, fbobj, gid):
		"""
		Parametri:
		* fbobj: un oggetto Facebook
		* gid: il numero che identifica un gruppo su Facebook
		"""
		super(Group, self).__init__(fbobj)
		self.__set_gid (gid)

	def get_gid(self):
		"""Restituisce l'id di questo gruppo"""
		return self.__gid

	def __set_gid(self, gid):
		"""
		ATTENZIONE: QUESTO METODO DEVE ESSERE CHIAMATO SOLO UNA VOLTA DA __init__()
		Questo oggetto rappresenta un preciso gruppo, il gid non deve essere modificato
		"""
		self.__gid = str(gid)

	def get_members(self, out=sys.stderr, verbose=False, processes=1, queue_get_timeout=5):
		"""
		Restituisce la lista dei membri, ogni membro è un dizionario con varie
		informazioni

		Parametri:
		* out: dove verrà mostrato il contatore dei download (stdout/stderr/...),
		  attivabile con verbose
		* verbose: scrive su out il numero di profili attualmente scaricati
		* processes: il numero di processi da utilizzare per il download
		  ATTENZIONE: Attualmente usando troppi processi Facebook potrebbe dare
		  un errore di login per i troppi tentativi; inoltre questo potrebbe
		  rallentare invece che velocizzare, visto che ogni processo deve rifare
		  il login
		* queue_get_timeout: quanti secondi aspettare che arrivi un profilo
		  dai processi, prima di considerare i profili finiti
		"""

		# verranno scaricate delle pagine con una lista di profili in ogni pagina

		# una coda con i profili, utilizzabile da più processi contemporaneamente
		members_q = multiprocessing.Queue()

		# Costante da aggiungere al parametro "start" nell'url per andare
		# alla pagina successiva
		# Si potrebbe anche cercare il link, ma è più comodo così per dividere
		# il lavoro fra più processi
		start_offset = None

		# cerca il valore di start_offset
		# scarica la prima pagina
		# XXX Usare args in get2
		pag1 = "https://m.facebook.com/browse/group/members/?id=%s&start=0" % self.gid
		logger.debug("Looking for the value of start_offset, downloading pag1")
		pag = self.session.get2(pag1)
		bspag = BeautifulSoup(pag.text, "lxml")

		try:
			# cerca il link alla pagina successiva
			pag2 = bspag.find("div", attrs={'id': "m_more_item"}).a.get("href")
			# se non c'è stata un eccezione, ha trovato il link ed estrae il numero
			start_offset = int(pag2[pag2.find("start="):].split("=")[1].split("&")[0])
			logger.debug("start_offset = %d", start_offset)
		except AttributeError:
			# AttributeError: 'NoneType' object has no attribute 'a'
			# il link non è stato trovato, è una sola pagina
			logger.debug("Link to the next page not found")

		# se c'è una sola pagina non ha senso usare più processi
		if start_offset is None:
			logger.debug("One page download")
			self.__members_download_process(members_q, self.session, start_offset=0, start=0)
		else:
			# un solo processo equivale a chiamare normalmente il metodo
			if processes == 1:
				logger.debug("Single process download")
				self.__members_download_process(members_q, self.session, start_offset, start=0)
			else:
				logger.debug("Multiprocess download")

				# lista dei processi
				proc_l = []
				# valore di start per il processo
				proc_start = 0
				# start_offset per i processi
				p_start_offset = int(start_offset) * int(processes)

				# creazione dei processi
				for i in range(0, processes):
					logger.debug("Creating process %s" % (i + 1))

					# HACK Crea una nuova sessione/oggetto Facebook per ogni processo
					# Sarebbe meglio usare una sola sessione (che abbiamo già)
					# Ma sembra che non sia utilizzabile con più processi contemporaneamente
					# SSLError: [Errno 1] _ssl.c:1429: error:140943FC:SSL routines:SSL3_READ_BYTES:sslv3 alert bad record mac

					# TODO Al massimo aggiungere la gestione di più sessioni
					# nell'oggetto Facebook
					# in modo da non perderle, che sono lente da creare, e fb
					# da errore se si fa il login troppo frequentemente

					tmp_fb = Facebook(self.fbobj.email, self.fbobj.password)
					tmp_session = tmp_fb.session
					# creazione di un processo
					proc_args = (members_q, tmp_session, p_start_offset, proc_start)
					tmp_proc = multiprocessing.Process(target=self.__members_download_process, args=proc_args)
					# per ora mettiamo il processo nella lista, si avviano dopo
					proc_l.append(tmp_proc)
					# il prossimo processo deve partire dalla pagina successiva
					proc_start += start_offset

				# avvio dei processi
				for process in proc_l:
					logger.debug("Starting process %s" % (proc_l.index(process) + 1))
					process.start()

		# ora riceviamo i profili
		try:
			members_l = []

			# TODO Fare un test per vedere come è più veloce
			# il numero di profili potrebbe essere ricavato con len()
			# ma ho paura che ci metta meno a fare
			# profili += 1
			# print profili
			# che
			# print len(members_l)
			# La differenza probabilmente è piccola, ma siamo in un ciclo
			profili = 0

			# "riceve" i profili e li aggiunge a members_l
			logger.debug("Waiting for profiles, timeout %s" % queue_get_timeout)
			while(True):
				try:
					# TODO Inviare un qualcosa di particolare per dire che
					# i profili sono finiti, eliminare il timeout
					tmp_prof = members_q.get(timeout=queue_get_timeout)
				except Queue.Empty:
					logger.debug("Queue empty")
					break

				members_l.append(tmp_prof)
				profili += 1

				if verbose:
					# XXX Come unire questo output e quello di logging?
					# È brutto così :(
					out.write("Profili scaricati: %s\r"  % profili)
					out.flush()

		except KeyboardInterrupt:
			logger.warning("Parent received ctrl-c")

			# terminiamo i processi
			for process in proc_l:
				process.terminate()
				process.join()

			# ed usciamo
			# (o è meglio usare solo return?)
			exit()

		if verbose:
			# per il contatore dei profili
			# perché fino a ora ho riscritto la stessa riga con \r
			out.write("\n")

		return members_l

	def __members_download_process(self, queue, session, start_offset, start):
		"""
		Metodo usato da self.get_members() per il download e l'estrazione dei profili
		Questo è un metodo separato in modo da poter usare più processi

		LA SESSIONE NON DEVE ESSERE LA STESSA PER PIÙ PROCESSI

		Parametri:
		* queue: l'oggetto multiprocessing.Queue() dove inviare i profili
		* start_offset: il numero da aggiungere a start per andare alla prossima
		  pagina da scaricare
		* start: il valore del parametro start nell'url
		"""

		# HACK È richiesta una sessione diversa per ogni processo a causa di questo errore
		# se si utilizza la stessa sessione
		# SSLError: [Errno 1] _ssl.c:1429: error:140943FC:SSL routines:SSL3_READ_BYTES:sslv3 alert bad record mac

		while(True):
			# TODO usare args={} in get2(), non questo schifo...
			# la pagina da scaricare con i profili
			pag_url = "https://m.facebook.com/browse/group/members/?id=%s&start=%s" % (self.gid, str(start))

			logger.debug("pid %d: start = %d", os.getpid(), start)
			pag = session.get2(pag_url)
			bspag = BeautifulSoup(pag.text, "lxml")

			# cerca i profili
			profili = bspag.body.find("div", attrs={'id': "root", 'role': "main"}).findAll("table")

			# nessun profilo nella pagina, pagine finite
			if len(profili) == 0:
				logger.debug("pid %d: there are no profiles in this pages", os.getpid())
				break

			#  estrae le informazioni
			for profilo in profili:
				try:
					#XXX Come restituire questi dati? Descrivere almeno il formato
					# del dizionario?
					profilo_info = {
									'inf': profilo.findAll("h3")[1].text,
									'name': profilo.find("h3").find("a").text,
									'img_src': profilo.find("img").get("src"),
									'table_id': profilo.get("id"),
									# [:-8] perché gli indirizzi finiscono con "?fref=pb"
									'profile_href': profilo.find("h3").find("a").get("href")[:-8]
									}
				except AttributeError:
					# 'NoneType' object has no attribute ...
					logger.error("Costante non trovata")
					logger.debug(str(profilo))
					raise

				if None in profilo_info.values():
					const_name = profilo_info.keys(profilo_info.values().index(None))
					err = "Costante non trovata: \"%s\" " % const_name
					logger.error(err)
					logger.debug(str(profilo))
					raise myexceptions.ConstError(err)

				# invia il profilo al processo principale
				queue.put(profilo_info)

			try:
				# cerca il link alla prossima pagina
				bspag.find("div", attrs={'id': "m_more_item"}).a.get("href")
			except AttributeError:
				# AttributeError: 'NoneType' object has no attribute 'a'
				# il link non è stato trovato
				logger.debug("pid %d: link to next page was not found", os.getpid())
				break

			start += start_offset

	# per avere un maggiore controllo sul download, usare il metodo
	members = property(get_members)
	gid = property(get_gid)


class Profile(GenericFBObj):
	"""Un profilo facebook"""

	def __init__(self, fbobj, url):
		"""
		Parametri:
		* fbobj:  un oggetto Facebook
		* url: dovrebbe essere nella forma "/usename", senza "facebook.com" prima
		"""

		super(Profile, self).__init__(fbobj)
		self.__set_url(url)

	def get_url(self):
		"""Restituisce l'url di questo profilo, nella forma  "/username"""
		return self.__url

	def __set_url(self, url):
		"""
		ATTENZIONE: QUESTO METODO DOVREBBE ESSERE USATO SOLO DA __init__()
		Questo oggetto rappresenta questo profilo, non deve essere modificato l'url

		Parametri:
		* url: dovrebbe essere nella forma "/username", senza "facebook.com" prima
		"""
		# TODO L'url se non sbaglio si può cambiare, servirebbe un id costante per
		# identificare solo quel profilo

		# se l'url non è nella forma giusta, convertiamolo
		if "facebook." in url.split("/")[0]:
			url = "/" + url.split("/")[1]

		self.__url = url

	def get_gender(self):
		"""AL ROKO AL ROKO!!1"""
		# Stringa da cercare nel codice HTML, cambia con la lingua
		gender_title = {'Italiano': "Sesso", 'English (US)': "Gender"}
		info_url = "https://m.facebook.com" + self.url + "?v=info"

		# scarica la pagina delle informazioni
		logger.debug("Downloading info page")
		pag = self.session.get2(info_url)

		try:
			# cerca nella pagina
			b = BeautifulSoup(pag.text, "lxml")
			attrs = {'title': gender_title[self.fbobj.lang]}
			gender =  b.find("div", attrs=attrs).findAll("div")[1].text
			logger.debug("gender = %s" % gender)
			return gender
		except AttributeError:
			# Non trovato
			logger.debug("Gender not found")
			return "bho"
		except KeyError:
			e = "Il metodo Profile.get_gender() non può funzionare con la lingua del profilo, deve essere aggiornato"
			d = "Il dizionario \"gender_title\" non ha una stringa per la lingua del profilo, aggiungerla"

			logger.error(e)
			logger.debug(d)
			logger.debug("Lingua: %s", self.fbobj.lang)

			raise KeyError(d)

	#XXX Un altro modo per scegliere la dimensione? Questo non mi convince
	def get_profile_picture_link(self, size="medium"):
		"""
		Restituisce il link all'immagine del profilo, o una stringa vuota
		in caso di errore

		Parametri:
		* size: la grandezza dell'immagine, accetta come valore "small", "medium"
		  e "large"
		"""
		# Titolo dell'album con le immagini del profilo
		profile_pictures_text = {
								'English (US)': "Profile Pictures",
								'Italiano': "Immagini del profilo"
								}
		# La prima pagina con la lista degli album, ce ne sono anche altri
		# ma a noi bastano questi, l'album dovrebbe essere all'inizio
		album_list_url = "https://m.facebook.com" + self.url + "/photos"
		size = size.lower()

		# HACK Non implementati
		# TODO Finire
		if (size == "small") or (size == "large"):
			logger.warning("Method not implemented for size \"%s\", using \"medium\"", size)
			size = "medium"
		if  size == "medium":
			logger.debug("Downloading album list")
			pag = self.session.get2(album_list_url)

			# profile pictures
			pp_url = None

			# cerca l'album
			for link in BeautifulSoup(pag.text, "lxml").findAll("a"):
				try:
					if profile_pictures_text[self.fbobj.lang] in link.text:
						pp_url = "https://m.facebook.com" + link.get("href")
						logger.debug("pp_url = %s" % pp_url)
						break
				except KeyError:
					e = "Il metodo Profile.get_profile_picture_link() non può funzionare con la lingua del profilo, aggiornarlo"
					d = "Costante mancante in \"profile_pictures_text\" per la lingua del profilo, aggiungerla"

					logger.error(e)
					logger.debug(d)
					logger.debug("Lingua: %s", self.fbobj.lang)

					raise KeyError(d)

			if pp_url is None:
				e = "Album \"%s\" non trovato!" % profile_pictures_text[self.fbobj.lang]

				logger.error(e)
				logger.debug("url %s", album_list_url)

				raise myexceptions.ConstError(e, album_list_url)

			# scarica l'album
			logger.debug("Downloading album")
			pag = self.session.get2(pp_url)

			# trova l'immagine più recente
			try:
				b = BeautifulSoup(pag.text, "lxml")
				latest_url = b.find("div", attrs={'id': "thumbnail_area"}).find("a").get("href")
				latest_url = "https://m.facebook.com" + latest_url
				logger.debug("Latest image = %s" % latest_url)
			except AttributeError:
				# 'NoneType' object has no attribute 'get'
				# A volte l'album è vuoto
				logger.debug("Album empty")
				return ""

			# va alla pagina dell'anteprima
			logger.debug("Downloading preview of latest image")
			pag = self.session.get2(latest_url)

			# estrae il link dell'anteprima visualizzata in questa pagina
			b = BeautifulSoup(pag.text, "lxml")
			return b.find("div", attrs={'id': "root"}).find("img").get("src")
		else:
			logger.warning("Profile.get_profile_picture_link(): invalid size \"%s\"", size)

	gender = property(get_gender)
	# immagine di medie dimensioni, per altre dimensioni usare il metodo
	profile_picture = property(get_profile_picture_link)
	url = property(get_url)


def ruba(email, password):
	""" Paura eh? xD """
	pass
