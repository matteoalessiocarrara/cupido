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

""" Componenti di un filtro """

import logging


import version


# Configurazione del sistema di logging
logger = logging.getLogger(version.lib_name)
logger.addHandler(logging.NullHandler())


class FilterRules(object):
	"""Le regole di un filtro, ovvero la definizione di cosa può passare dal filtro"""
	
	# TODO Gestire  meglio traduzioni stringhe
	
	
	# Queste proprietà verranno controllate con test basati sull'uguaglianza
	
	# Ogni key deve essere il nome di un attributo di un oggetto lib.htmlfbapi.fbobj.Profile
	# Il valore di ogni key viene confrontato con il valore del corrispondente attributo
	# usando ==
	# Per confronti diversi dall'uguaglianza, usare i due metodi sotto
	required_property_for_equality_test = {}
	optional_property_for_equality_test = {}
	
	
	# Qui è possibile definire test personalizzati, se i test basati sull'uguaglianza
	# non fossero sufficienti
	
	def required_property_custom_test(self, profile):
		"""
		Controlla se il profilo soddisfa i requisiti richiesti, con dei test 
		personalizzati
		Restituisce True o False
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		# Se non ci sono test, allora soddisfa i requisiti richiesti (nessuno)
		ok = True
	
		# ATTENZIONE: Deve sempre restituire qualcosa, anche quando non ci sono controlli
		return ok
		
	def optional_property_custom_test(self, profile):
		"""
		Controlla quali requisiti opzionali sono soddisfatti dal profilo, con dei test
		personalizzati
		Restituisce una lista con i nomi dei requisiti soddisfatti
		
		Parametri:
		
			profile: lib.htmlfbapi.fbobj.Profile
				Il profilo da controllare
		"""
		
		l = []
	
		# ATTENZIONE: Deve sempre restituire una lista, anche quando non ci sono controlli
		return l
		
