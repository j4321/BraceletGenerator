#! /usr/bin/python3
# -*- coding:Utf-8 -*-
"""
Bracelet Generator - An easy way to design friendship bracelet patterns
Copyright 2014-2017 Juliette Monsel <j_4321@protonmail.com>

Bracelet Generator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Bracelet Generator is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

main
"""

import sys
import os
from BraceletGenerator.constantes import CONFIG
from BraceletGenerator.bracelet import Bracelet

if len(sys.argv) == 1:
    Bracelet(string_nb=CONFIG.getint("Bracelet", "string_nb"),
             row_nb=CONFIG.getint("Bracelet", "row_nb"),
             color=CONFIG.get("Bracelet", "default_color"))
else:
    fichier = os.path.realpath(sys.argv[1])
    Bracelet(fichier=fichier)

