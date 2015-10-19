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
from sys import argv

if len(argv) != 3 + 1:
	exit("Uso: " + argv[0] + " username password id_gruppo")

gid = argv[3]
user = argv[1]
passw = argv[2]

fb = htmlfbapi.Facebook(user, passw)
membri = fb.get_group(gid).members()

for profilo in membri:
	if fb.get_profile(profilo['profile_href']).gender() == "Donna":
		print profilo['profile_href']
