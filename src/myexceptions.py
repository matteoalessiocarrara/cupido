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

"""Eccezioni della libreria"""

import logging

# configurazione del sistema di logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ConstError(Exception):
	"""Il codice prima funzionava e ora non funziona più, una "costante" è cambiata"""
	pass


class LoginError(Exception):
	"""Login rifiutato da fb"""

	def __init__(self, message, res_title, res_text, email, password, *args):
		"""
		Parametri:
		* res_title dovrebbe essere il titolo della pagina HTML restituita
		* res_text l'HTML della pagina restituita
		"""
		# without this you may get DeprecationWarning
		self.message = message

		self.res_title = res_title
		self.res_text = res_text
		self.email = email
		self.password = password

		# allow users initialize misc. arguments as any other builtin Error
		super(LoginError, self).__init__(message, res_title, res_text, email, password, *args)
