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

from sys import argv

if len(argv) != 1 + 1:
	exit("Uso: " + argv[0] + " url_gruppo")

url = argv[1]
gid = None

# m.facebook.com, https
if "https://m.facebook.com/groups/" in url:
	gid = url[len("https://m.facebook.com/groups/"):url.find("?")]
# www.facebook.com, https
elif "https://www.facebook.com/groups/" in url:
	gid = url[len("https://www.facebook.com/groups/"):url.find("?")]
else:
	exit("Gid non trovato, controlla se l'indirizzo è giusto")

print gid
