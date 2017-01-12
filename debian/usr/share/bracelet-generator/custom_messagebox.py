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


Custom tkinter messageboxes
"""

from tkinter import Toplevel, BooleanVar, Tk
from tkinter.ttk import Label, Button, Style, Checkbutton

class OBCheckbutton(Tk):
    """ Messagebox with only one button and a checkbox below the button
        for instance to add a 'Do not show this again' option """

    def __init__(self, title="", message="", button="Ok", image=None,
                 checkmessage="", style="clam", **options):
        """
            Create a messagebox with one button and a checkbox below the button:
                parent: parent of the toplevel window
                title: message box title
                message: message box text
                button: message displayed on the button
                image: image displayed at the left of the message
                checkmessage: message displayed next to the checkbox
                **options: other options to pass to the Toplevel.__init__ method
        """
        Tk.__init__(self, **options)
        self.title(title)
        self.resizable(False, False)
        s = Style(self)
        s.theme_use(style)
        if image:
            Label(self, text=message, wraplength=335,
                  font="Sans 11", compound="left", image=image).grid(row=0, padx=10, pady=(10,0))
        else:
            Label(self, text=message, wraplength=335,
                  font="Sans 11").grid(row=0, padx=10, pady=(10,0))
        b = Button(self, text=button, command=self.destroy)
        b.grid(row=2, padx=10, pady=10)
        self.var = BooleanVar(self)
        c = Checkbutton(self, text=checkmessage, variable=self.var)
        c.grid(row=1, padx=10, pady=0, sticky="e")
        self.grab_set()
        b.focus_set()
        self.wait_window(self)

    def get_check(self):
        return self.var.get()

def ob_checkbutton(title="", message="", button="Ok", image=None,
                   checkmessage="", style="clam", **options):
    """ Open a OBCheckbutton and return the value of the checkbutton when closed. """
    ob = OBCheckbutton(title, message, button, image, checkmessage, style, **options)
    return ob.get_check()
