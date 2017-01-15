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

Add ghostscript to the path variable in Windows
"""

from BraceletGenerator.constantes import os, PL
from subprocess import call
from tkinter import Tk
from tkinter.messagebox import showerror, showinfo

if PL == "nt":
    gs = False
    if os.path.exists("C:\\Program Files") and "gs" in os.listdir("C:\\Program Files"):
        l = [i for i in os.listdir("C:\\Program Files\\gs") if "gs" in i]
        if l:
            i = 0
            while i < len(l) and not "bin" in os.listdir(os.path.join("C:\\Program Files\\gs", l[i])):
                i += 1
            if i < len(l):
                gs = True
                gspath = os.path.join("C:\\Program Files\\gs", l[i], "bin")
    if not gs:
        if os.path.exists("C:\\Program Files (x86") and "gs" in os.listdir("C:\\Program Files (x86)"):
            l = [i for i in os.listdir("C:\\Program Files (x86)\\gs") if "gs" in i]
            if l:
                i = 0
                while i < len(l) and not "bin" in os.listdir(os.path.join("C:\\Program Files (x86)\\gs", l[i])):
                    i += 1
                if i < len(l):
                    gs = True
                    gspath = os.path.join("C:\\Program Files (x86)\\gs", l[i], "bin")

    if not gs:
        root = Tk()
        root.withdraw()
        showerror(_("Error"), 
                  _("Ghostscript has not been not found, you won't be able to export patterns to .png or .jpeg unless you install it. If Ghostscript is installed, try to manually add its location to the system path variable with 'setx path %path%;path\\to\\gs\\bin'."))
    else:
        call(["setx", "path", "%path%;" + gspath])
        root = Tk()
        root.withdraw()
        showinfo(_("Information"),
                 _("Ghostscript has been found, you will be able to export patterns to .png or .jpeg."))
