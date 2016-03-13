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

""" Informazioni sul software """


from lib.figafind.src import version as libversion
import version


logo = \
"                                          \n"\
"  █████▒  █████▒ ██▓ ███▄    █ ▓█████▄   \n"\
"▓██   ▒ ▓██   ▒ ▓██▒ ██ ▀█   █ ▒██▀ ██▌        \n"\
"▒████ ░ ▒████ ░ ▒██▒▓██  ▀█ ██▒░██   █▌ \n"\
"░▓█▒  ░ ░▓█▒  ░ ░██░▓██▒  ▐▌██▒░▓█▄   ▌  \n"\
"░▒█░    ░▒█░    ░██░▒██░   ▓██░░▒████▓     \n"\
" ▒ ░     ▒ ░    ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒                      \n"\
" ░       ░       ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒                         \n"\
" ░ ░     ░ ░     ▒ ░   ░   ░ ░  ░ ░  ░                          \n"\
"                 ░           ░    ░                           \n"\
"                                ░                 \n"\
"                                          \n"\
"FigaFind v. 6.9                           \n"\

sw_name = "FigaFind"


# Informazioni per --version
v = '%s %s\n' % (sw_name, version.version_str)
v += "lib figafind version %s\n" % libversion.version_str
v += "Copyright (C) 2015 - 2016 Matteo Alessio Carrara\n"
v += "License GPLv2: GNU GPL version 2 <http://www.gnu.org/licenses/gpl-2.0.html>\n\n"
v += "This is free software: you are free to change and redistribute it.\n"
v += "There is NO WARRANTY, to the extent permitted by law."


# Epilog, per --help
e = "Report bugs to: <https://github.com/matteoalessiocarrara/FigaFind/issues>\n"
e += sw_name + " home page: <https://github.com/matteoalessiocarrara/FigaFind>"
