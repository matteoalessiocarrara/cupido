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

""" Oggetto principale """

import logging


from lib.fbwrapper.src import fbwrapper
from lib.fbwrapper.src import version as fbwrapper_version
from lib.fbwrapper.src.shared import caching_levels


import version
import fbobj


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Migliorare il sistema di controllo della versione
# fbwrapper.version.major.require()
if fbwrapper_version.version_major != version.fbwrapper_version_required:
	name = fbwrapper_version.lib_name
	required = version.fbwrapper_version_required
	found = fbwrapper_version.version_major
	e = "Versione di %s incompatibile, richiesta %s, trovata %s" % (name, required,
																	found)
	raise NotImplementedError(e)


class Facebook(fbwrapper.Facebook):
	"""Il sito, visto da un profilo"""
	
	def __init__(self, email, password, human_emulation_enabled=True,
				caching_level=caching_levels['disabled']):
					
		# Tenere sincronizzata con la docstring con quella di fbwrapper.Facebook.__init__()
		"""
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
				shared.caching_levels
		"""
		
		# Usiamo la nostra classe fbobj.Profile
		super(Facebook, self).__init__(email, password, profile_class=fbobj.Profile,
										human_emulation_enabled=human_emulation_enabled,
										caching_level=caching_level)

	def get_profile(self, url):
		# Tenere sincronizzata con la docstring di fbwrapper.Facebook.get_profile()
		"""
		Restituisce un oggetto fbobj.Profile
		
		Parametri:
		
			url: str
				Url completo del profilo, es: https://m.facebook.com/profilo
		"""
		
		return fbobj.Profile(self, url)
