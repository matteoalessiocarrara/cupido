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

import logging
import sys


format_debug = "%(asctime)s %(levelname)s %(name)s: %(filename)s: %(lineno)d: %(funcName)s: pid %(process)d: %(message)s"
format_info = "%(levelname)s %(name)s: %(funcName)s: %(message)s"
format_warning = "%(levelname)s %(name)s: %(message)s"


def logging_config(level=logging.INFO):
	rootlogger = logging.getLogger()
	rootlogger.setLevel(level)
	
	
	# Rimuoviamo i precedenti handler
	
	handlers = tuple(rootlogger.handlers)
	
	for handler in handlers:
		rootlogger.removeHandler(handler)


	# Create console handler and set level to debug
	ch = logging.StreamHandler(stream=sys.stderr)
	ch.setLevel(logging.DEBUG)


	# Create formatter
	formatter = None
	
	if level == logging.DEBUG:
		formatter = logging.Formatter(format_debug)
		
	elif level == logging.INFO:
		formatter = logging.Formatter(format_info)
		
	else:
		formatter = logging.Formatter(format_warning)


	# Add formatter to ch
	ch.setFormatter(formatter)

	# Add ch to logger
	rootlogger.addHandler(ch)
