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

"""Versione modificata di requests, usata nella libreria"""

import requests
import logging

# configurazione del sistema di logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class Session(requests.Session):
	"""Aggiunge il metodo get2() a request.Session()"""

	def get2(self, url, **kwargs):
		"""Crea un eccezione requests.HTTPError in caso di errore"""

		ret = self.get(url, **kwargs)

		try:
			ret.raise_for_status()
		except requests.HTTPError as e:
			logger.error("requests.HTTPError: url = %s, message = %s ", url, e.message)
			logger.debug("requests.HTTPError: args = %s", e.args)
			logger.debug("requests.HTTPError: ret.text = %s", ret.text)
			raise

		return ret
