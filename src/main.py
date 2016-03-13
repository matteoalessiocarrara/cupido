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

"""Cerca le ragazze in un gruppo su Facebook"""

# TODO Controllare versione librerie

from getpass import getpass
from sys import stdout, stderr

import argparse
import logging


from lib.figafind.src.figafind import figafind
from lib.figafind.src.lib.htmlfbapi.src.lib.fbwrapper.src.shared import caching_levels


from logging_config import logging_config

import version
import info


# Attenzione: considerare sempre che l'output potebbe essere ridirezionato in un file,
# quindi evitare di scrivere su stdout


def main():

	print >>stderr, info.logo

	
	if args.interactive:
		# Evitiamo domande/segnalazioni di bug con "Perché non scrive?????"
		logger.warning("Username e password non saranno ripetuti sullo schermo")
		print >>stderr, ""
		
		username = getpass(prompt="Username: ", stream=stderr)
		password = getpass(prompt="Password: ", stream=stderr)
	
		print >>stderr, "Url del gruppo: ",
		group_url = raw_input()
		print >>stderr, ""
	
	else:
		username = args.username
		password = args.password
		group_url = args.group_url
	
		if (username == None) or (password == None) or (group_url == None):
			e = "--username, --password e --group-url sono richiesti, se non è specificato il parametro --interactive"
			raise ValueError(e)
	
		# Nascondiamo la password, altrimenti rimane visibile sul terminale
		# FIXME Il clear si vede nell'output, se viene ridirezionato in un file
		# XXX È comunque un brutto modo per pulire lo schermo
		# os.system("clear")
	
	
	if args.gay:
		logger.warning("Omosessuale rilevato! I tuoi dati saranno inviati alla Chiesa, perché possa salvarti")
		logger.warning("\"Allora l’Eterno fece piovere dal cielo su Sodoma e Gomorra zolfo e fuoco, da parte dell’Eterno.\" (Genesi 19:24)")
		
	
	ragazze = figafind(username, password, group_url, not args.disable_human_emulation,
						args.caching_level, args.processes, gay=args.gay)
	
	
	# Stampiamo su stdout le ragazze trovate, l'output può essere ridirezionato in un file
	for figa in ragazze:
		print figa['url'], figa['name']
		

def argparse_init():
	global args
	
	caching_level_help = "Specifica quanto usare la cache. I possibili valori sono:\n"
	caching_level_choices = []
	
	for level in caching_levels:
	       caching_level_help += "%s: %s\n" % (caching_levels[level], level)
	       caching_level_choices.append(caching_levels[level])
	 
	
	# Argparse formatter class
	f = argparse.RawDescriptionHelpFormatter
	
	# XXX L'output sembra sia automaticamente convertito per un terminale di 80
	# colonne, anche quando il terminale è più grande
	parser = argparse.ArgumentParser(description=__doc__, epilog=info.e, formatter_class=f)
	
	
	# Questi verranno ignorati SOLO se è specificato --interactive
	parser.add_argument("--username", type=str, default=None)
	parser.add_argument("--password", type=str, default=None)
	parser.add_argument("--group-url", type=str, default=None)
	
	parser.add_argument("--8",  help="attiva la modalità per ghei", action="store_true", dest="gay")
	parser.add_argument("--processes", type=int, default=1)
	parser.add_argument("--disable-human-emulation", action="store_true",
						help="velocizza il software, ma facebook potrebbe rilevarci come bot")
	parser.add_argument("--caching-level", type=int, default=caching_levels['safe'],
						help=caching_level_help, choices=caching_level_choices)
	
	parser.add_argument("-i", "--interactive", action="store_true")
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	parser.add_argument("-d", "--debug", help="output più dettagliato di -v", action="store_true")
	
	parser.add_argument('--version', action='version', version=info.v)
	
	
	args = parser.parse_args()


def logging_init():
	# Di default lo mettiamo su warning, su info spamma parecchio perché ci sono tutte le lib
	logging_config(logging.WARNING)
	
	if args.verbose:
		logging_config(logging.INFO)
	if args.debug:
		logging_config(logging.DEBUG)



logger = logging.getLogger(info.sw_name)

argparse_init()
logging_init()
main()
