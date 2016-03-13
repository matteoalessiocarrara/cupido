#!/usr/bin/env python
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

import multiprocessing
import traceback
import logging
import time


from lib.htmlfbapi.src.lib.fbwrapper.src.shared import caching_levels
from lib.htmlfbapi.src import htmlfbapi
from lib.fbfilter.src import fbfilter

import requests


import filter_rules
import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Controllare versione librerie


def __filter_process_wrapper(kwargs):
	"""
	Wrapper per __filter_process, prende i parametri in un solo dizionario
	(utile con multiprocessing.Pool.map())
	
	Ci si aspetta che ci sia una key per ogni parametro di __filter_process
	"""
	
	# Tenere sincronizzato con i parametri di __filter_process
	email = kwargs['email']
	password = kwargs['password']
	human_emulation_enabled = kwargs['human_emulation_enabled']
	caching_level = kwargs['caching_level']
	sleep_before_login = kwargs['sleep_before_login']
	members = kwargs['members']
	fb = kwargs['fb']
	gay = kwargs['gay']
	
	return __filter_process(email, password, human_emulation_enabled, caching_level,
							sleep_before_login, members, fb, gay)
	
	
def __filter_process(email, password, human_emulation_enabled, caching_level, 
					sleep_before_login, members, fb, gay):
						
	# Tenere sincronizzata descrizone dei parametri con quella di htmlfbapi.Facebook.__init__()
	# Tenere sincronizzato sleep_before_login con la docstring di Group.get_members() di htmfbapi
	"""
	Prende una lista di persone, e controlla quali sono ragazze
	Restituisce una lista con i profili delle ragazze. Ogni profilo è un dizionario,
	il formato è quello del return di htmlfbapi.Facebook.get_group().get_members()
	
	Parametri:
	
		email: str
		
		password: str
		
		human_emulation_enabled: bool
			Attiva o disattiva la modalità di emulazione umana, che cerca di
			ingannare l'intelligenza artificiale di Facebook facendogli credere
			che il bot non è un bot
		
		caching_level: int
			È possibile usare una cache per evitare di dover recuperare troppo
			spesso alcune informazioni dal server. Questo velocizza la libreria,
			ma in alcuni casi i dati potrebbero essere non aggiornati.
			Sono disponibili vari livelli di caching, vedere il dizionario 
			lib.htmlfbapi.src.lib.fbwrapper.src.shared.caching_levels
	
		sleep_before_login: int
			Tempo di attesa fra il login di ogni processo. Può essere anche 0,
			ma molto probabilmente Facebook vi prenderà a calci in culo e si 
			bloccherà il programma con un errore di login
			
		members: list
			Lista dei profili da controllare, ci si aspetta che il formato dei 
			profili sia quello del return di htmlfbapi.get_group().get_members()
		
		fb: htmlfbapi.Facebook
			In fb si può specificare un oggetto Facebook già esistente se si ha,
			per evitare un nuovo login.
			Se è None, verrà creato un nuovo oggetto
			
		gay: bool
			Trasforma FigaFind i CazzoFind :)
	"""
	
	try:
		logger.info("Avviata la ricerca delle ragazze, profili da controllare: %s", len(members))
		
		if fb == None:
			logger.info("Creando un nuovo browser per il processo")
		
			# TODO Usare human emulation
			logger.info("Aspettando %ss prima del login", sleep_before_login)
			time.sleep(sleep_before_login)
			
			# TODO Usare finestre del browser
			# Usiamo un nuovo browser per ogni processo, non si può usare lo stesso con
			# più processi contemporaneamente perché da un qualche errore se si usa https
			fb = htmlfbapi.Facebook(email, password, human_emulation_enabled, caching_level)
		else:
			logger.info("Il browser è stato riutilizato")
	
		# Creiamo il filtro
		
		if not gay:
			filter_ = fbfilter.FbFilter(filter_rules.FigaFind(), email, password, fb=fb)
		else:
			filter_ = fbfilter.FbFilter(filter_rules.CazzoFind(), email, password, fb=fb)
	
		figa = []
		is_figa = lambda member: filter_.check(member['url'])['ok']
		
		
		for member in members:
			
			logger.info("Controllando %s", member['name'])
			
			try:
				if is_figa(member):
					figa.append(member)
					logger.info("Ragazza trovata: %s", member['name'])
					
			except requests.exceptions.HTTPError as e:
				
				# XXX Scrivere meglio
				if e.message == "500 Server Error: Internal Server Error":
					logger.warning("Saltato profilo %s: %s", member['url'], e.message) 
					
				else:
					raise
				
		return figa
	
	except Exception as e:
		
		# Questo perché se la funzione è eseguita in un processo, in caso di
		# eccezione non vengono stampate alcune informazioni
		traceback.print_exc()
		
		raise


def __create_sublist(list_, sublist):
	"""
	Divide list_ in sublist liste
	Restituisce una lista con sublist liste
	
	Parametri:
	
		list_: list
			La lista da dividere
			
		sublist: int
			In quante liste dividere list_
	"""
	
	ret = []
	
	# Numero di elementi per ogni sottolista
	sublist_items = len(list_) / sublist
	
	# Numero di elementi da aggiungere all'ultima sottolista
	last_sublist_items = len(list_) % sublist


	# TODO Migliorare algoritmo
	
	item_index = 0
	while item_index < len(list_):
		
		# Crea sublist sottoliste
		for sublist_index in range(0, sublist):
			this_sublist = []
			
			# Con sublist_items elementi in ognuna
			for i in range(0, sublist_items):
				this_sublist.append(list_[item_index])
				item_index += 1

			# Se è l'ultima sottolista
			if sublist_index == (sublist - 1):
				for i in range(0, last_sublist_items):
					this_sublist.append(list_[item_index])
					item_index += 1

			ret.append(this_sublist)
			
	return ret

# TODO Gestire meglio human emulation con multiprocessing
# TODO Assicurarsi che in caso di eccezioni, non perda i profili elaborati
def figafind(email, password, group_url, human_emulation_enabled=True, 
			caching_level=caching_levels['safe'], processes=1, sleep_before_login=5,
			gay=False):
	# Tenere sincronizzata descrizione del return con quella di __filter_process
	# Tenere sincronizzata descrizone dei parametri con quella di htmlfbapi.Facebook.__init__()
	# Tenere sincronizzato sleep_before_login e processes con la docstring di 
	# Group.get_members() di htmfbapi		
	"""
	Trova tutte le ragazze in un gruppo su Facebook
	Restituisce una lista di profili. Ogni profilo è un dizionario, il formato è
	quello del return di htmlfbapi.Facebook.get_group().get_members()
	
	Parametri:
	
		email: str
		
		password: str
		
		human_emulation_enabled: bool
			Attiva o disattiva la modalità di emulazione umana, che cerca di
			ingannare l'intelligenza artificiale di Facebook facendogli credere
			che il bot non è un bot
		
		caching_level: int
			È possibile usare una cache per evitare di dover recuperare troppo
			spesso alcune informazioni dal server. Questo velocizza la libreria,
			ma in alcuni casi i dati potrebbero essere non aggiornati.
			Sono disponibili vari livelli di caching, vedere il dizionario 
			lib.htmlfbapi.src.lib.fbwrapper.src.shared.caching_levels
	
		processes: int
			Il numero di processi da utilizzare per il download dei profili e 
			il successivo controllo
			ATTENZIONE: usando troppi processi Facebook potrebbe dare un errore
			di login per i troppi tentativi; inoltre questo potrebbe rallentare
			invece che velocizzare se ci sono pochi profili, visto che ogni processo
			deve rifare il login.
			
		sleep_before_login: int
			Tempo di attesa fra il login di ogni processo. Può essere anche 0,
			ma molto probabilmente Facebook vi prenderà a calci in culo e si 
			bloccherà il programma con un errore di login
	
		gay: bool
			Trasforma FigaFind i CazzoFind :)
	"""
	
	fb = htmlfbapi.Facebook(email, password, human_emulation_enabled, caching_level)
	group = fb.get_group(group_url)
	members = group.get_members(processes=processes, sleep_before_login=sleep_before_login)


	pool = multiprocessing.Pool(processes)
	
	# Divide la lista dei membri in liste più piccole, una per ogni processo
	processes_members = __create_sublist(members, processes)

	# Lista con i parametri per ogni processo
	processes_args = []
	
	# Creiamo la lista
						
	for process_n in range(0, processes):
		process_args = {
						'email': email,
						'password': password,
						'human_emulation_enabled': human_emulation_enabled,
						'caching_level': caching_level,
						'sleep_before_login': process_n * sleep_before_login,
						'members': processes_members[process_n],
						'gay': gay,
						
						# Riutilizziamo l'oggetto che abbiamo già, lo passiamo al 
						# primo processo
						# HACK FIXME Sembra che con multiprocessing non si possa
						# passare questo oggetto ad un nuovo processo O.o
						'fb': fb if processes == 1 else None
						}
						
		processes_args.append(process_args)

	
	figa = []
	
	# Se c'è un processo solo, chiamiamo direttamente il metodo... 
	# È utile per il debug, perché le eccezioni nella funzione eseguita con pool.map() 
	# sono troppo poco dettagliate

	if processes == 1:
		figa = __filter_process_wrapper(processes_args[0])
	
	else:
		logger.debug("Avviando i processi...")
		
		# Ogni processo restituisce una lista
		tmp_figa = pool.map(__filter_process_wrapper, processes_args)
	
		# Ora le liste di ogni processo devono essere unite
		
		for list_ in tmp_figa:
			figa += list_


	return figa
