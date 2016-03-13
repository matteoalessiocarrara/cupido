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

# Questa dovrebbe essere una classe, ma non può esserlo direttamente perché
# la classe FilterRules dal quale deriva deve essere variabile

""" Il filtro """

import logging


from lib.htmlfbapi.src import htmlfbapi
from lib.htmlfbapi.src import version as htmlfbapi_version
from lib.htmlfbapi.src.lib.fbwrapper.src.shared import caching_levels


import filter_components
import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Migliorare il sistema di controllo della versione
# htmlfbapi.version.major.require()
if htmlfbapi_version.version_major != version.htmlfbapi_version_required:
	name = htmlfbapi_version.lib_name
	required = version.htmlfbapi_version_required
	found = htmlfbapi_version.version_major
	e = "Versione di %s incompatibile, richiesta %s, trovata %s" % (name, required,
																	found)
	raise NotImplementedError(e)

		
class FbFilter(object):
		
	def __init__(self, rules, username, password, human_emulation_enabled=True,
				caching_level=caching_levels['disabled'], fb=None):
		
		# Tenere sincronizzata la docstring con quella di htmlfbapi.Facebook.__init__()
		"""
		Si connette a facebook, per poter controllare i profili che verranno poi
		passati.
		È possibile utilizzare un oggetto htmlfbapi.Facebook già esistente, passandolo
		in fb.
	
		Parametri:
		
			rules: filter_components.FilterRules
				Regole del filtro, classe derivata da filter_components.FilterRules
				
			username: str
			
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
				shared.caching_levels
				
			fb: htmlfbapi.Facebook
				Può essere utilizzato un oggetto htmlfbapi.Facebook già esistente
				se si ha, per evitare di dover rifare il login. Se viene specificato
				questo parametro, i parametri relativi ad un nuovo login (username,
				password, human_emulation_enabled ecc) saranno ignorati
		"""

		if fb == None:
			self.fb = htmlfbapi.Facebook(username, password, human_emulation_enabled,
										caching_level)
		else:
			self.fb = fb
			
		self.rules = rules
	
	# Questi due metodi sono inclusi in self.rules per necessità, ma a livello logico
	# dovrebbero essere in questo oggetto
		
	def required_property_custom_test(self, profile):
		# Tenere sincronizzata la docstring con quella di 
		# filter_components.FilterRules.required_property_custom_test()
		"""
		Controlla se il profilo soddisfa i requisiti richiesti, con dei test 
		personalizzati
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		logger.info("Eseguendo il test personalizzato sulle proprietà richieste")
		return self.rules.required_property_custom_test(profile)
		
	def optional_property_custom_test(self, profile):
		# Tenere sincronizzata la docstring con quella di 
		# filter_components.FilterRules.optional_property_custom_test()		
		"""
		Controlla quali requisiti opzionali sono soddisfatti dal profilo, con dei test
		personalizzati
		Restituisce una lista con i nomi dei requisiti soddisfatti
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		logger.info("Eseguendo il test personalizzato sulle proprietà opzionali")
		return self.rules.optional_property_custom_test(profile)
		
	def required_property_equality_test(self, profile):
		"""
		Controlla le proprietà richieste, test basato sull'uguaglianza
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		logger.info("Eseguendo il test basato sull'uguaglianza per le proprietà richieste")
		
		for property_name in self.rules.required_property_for_equality_test:
			logger.debug("Controllando la proprietà %s", property_name)

			required = self.required_property_for_equality_test[property_name]
			obtained = profile.__getattribute__(property_name)
			
			if not (required == obtained):
				logger.debug("Test fallito, %s != %s", required, obtained)
				return False
		
		return True
		
	def optional_property_equality_test(self, profile):
		"""
		Controlla le proprietà opzionali, test basato sull'uguaglianza
		Restituisce una lista con i nomi dei requisiti soddisfatti
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		logger.info("Eseguendo il test basato sull'uguaglianza per le proprietà opzionali")
		
		ret = []
		
		for property_name in self.rules.optional_property_for_equality_test:
			logger.debug("Controllando la proprietà %s", property_name)

			required = self.optional_property_for_equality_test[property_name]
			obtained = profile.__getattribute__(property_name)
			
			if required == obtained:
				logger.debug("Proprietà opzionale aggiunta, %s", property_name)
				ret.append(property_name)
		
		return ret
		
	def check_required_property(self, profile):
		"""
		Controlla se il profilo soddisfa i requisiti richiesti
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		if self.required_property_equality_test(profile) == True:
			if self.required_property_custom_test(profile) == True:
				return True
		
	def check_optional_property(self, profile):
		"""
		Controlla quali requisiti opzionali sono soddisfatti dal profilo
		Restituisce una lista con i nomi dei requisiti soddisfatti
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		return self.optional_property_equality_test(profile) + self.optional_property_custom_test(profile)
	
	def check(self, profile_url):
		# Tenere descrizione sincronizzata con htmlfbapi.Facebook.get_profile()
		"""
		Controlla se il profilo soddisfa i requisiti del filtro
		
		Parametri:
			
			profile_url: str
				Url completo del profilo, es: https://m.facebook.com/profilo
		
		Restituisce un dizionario
		
		Keys:
		
			ok: bool
				Il profilo soddisfa i requisiti richiesti
			
			opt: list
				Lista dei requisiti opzionali soddisfatti, viene creata solo se
				il profilo soddisfa i requisiti richiesti
		"""
		
		logger.info("Controllando il profilo %s", profile_url)
	
		profile = self.fb.get_profile(profile_url)
	
		ok = self.check_required_property(profile)
		optional_property_list = []
		
		if ok:
			optional_property_list = self.check_optional_property(profile)
		
		return {'ok': ok, 'opt': optional_property_list}
