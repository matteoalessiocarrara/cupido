#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from lib.HTML_Facebook_API.src import htmlfbapi
from sys import stdout
from getpass import getpass

print ""
print "  █████▒  █████▒ ██▓ ███▄    █ ▓█████▄ "
print "▓██   ▒ ▓██   ▒ ▓██▒ ██ ▀█   █ ▒██▀ ██▌"
print "▒████ ░ ▒████ ░ ▒██▒▓██  ▀█ ██▒░██   █▌"
print "░▓█▒  ░ ░▓█▒  ░ ░██░▓██▒  ▐▌██▒░▓█▄   ▌"
print "░▒█░    ░▒█░    ░██░▒██░   ▓██░░▒████▓ "
print " ▒ ░     ▒ ░    ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ "
print " ░       ░       ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒ "
print " ░ ░     ░ ░     ▒ ░   ░   ░ ░  ░ ░  ░ "
print "                 ░           ░    ░    "
print "                                ░      "
print ""
print "FigaFind v. 0.6.9"
print ""

user = raw_input("Username: ")
passw = getpass()
gid = raw_input("Gruppo (id): ")

stdout.write("\nLogin in corso...")
stdout.flush()

fb = htmlfbapi.Facebook(user, passw)

print "                                                        [ OK ] "
print "Attivazione modalità M.D.F...                                            [ OK ] "
print "Creazione variabili fittizie...                                          [ OK ] "
print "Scaricamento lista dei partecipanti..."

membri = fb.get_group(gid).members(verbose=True)
membri_len = len(membri)

print "Ricerca tette in corso..."

for profilo in membri:
	stdout.write(str(membri.index(profilo)) + "/" + str(membri_len) + "...\r")
	stdout.flush()
	if fb.get_profile(profilo['profile_href']).gender() == fb.gender_str("female"):
		print " * " + profilo['profile_href'], "(" + profilo['name'] + ")"
