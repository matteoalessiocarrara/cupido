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

""" Regole per il filtro lib.fbfilter.src.fbfilter.FbFilter """

import logging


from lib.fbfilter.src import filter_components


import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


# TODO Controllare versione librerie


class FigaFind(filter_components.FilterRules):

	def required_property_custom_test(self, profile):
		# Tenere docstring sincronizzata con quella di
		# filter_components.FilterRules.required_property_custom_test()
		"""
		Controlla se il profilo soddisfa i requisiti richiesti, con dei test 
		personalizzati
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		try:
			ok = (profile.gender['Italiano'] == "Donna")
		
		except KeyError:
			ok = False
			logger.warning("Impossibile valutare il genere di %s, perché '%s' non ha una traduzione in Italiano", profile.nickname, profile.gender[profile.fbobj.my_profile.lang])
	
		return ok


class CazzoFind(filter_components.FilterRules):
	
	def required_property_custom_test(self, profile):
		# Tenere docstring sincronizzata con quella di
		# filter_components.FilterRules.required_property_custom_test()
		"""
		Controlla se il profilo soddisfa i requisiti richiesti, con dei test 
		personalizzati
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		try:
			ok = (profile.gender['Italiano'] == "Uomo")
		
		except KeyError:
			ok = False
			logger.warning("Impossibile valutare il genere di %s, perché '%s' non ha una traduzione in Italiano", profile.nickname, profile.gender[profile.fbobj.my_profile.lang])
	
		return ok
	
