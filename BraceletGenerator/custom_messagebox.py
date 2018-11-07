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


from tkinter import BooleanVar, Tk, PhotoImage, TclError
from tkinter.ttk import Label, Button, Checkbutton, Style
from BraceletGenerator.constantes import STYLE


class OBCheckbutton(Tk):
    """ Messagebox with only one button and a checkbox below the button
        for instance to add a 'Do not show this again' option """

    def __init__(self, title="", message="", button="Ok", image=None,
                 checkmessage="", **options):
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
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        style = Style(self)
        style.theme_use(STYLE)
        self.img = None
        if isinstance(image, str):
            try:
                self.img = PhotoImage(file=image)
            except TclError:
                self.img = PhotoImage(data=image)
        elif image:
            self.img = image
        if self.img:
            Label(self, image=self.img).grid(row=0, column=0, padx=10, pady=(10, 0))
        Label(self, text=message, wraplength=335,
              font="TkDefaultFont 10 bold").grid(row=0, column=1,
                                                 padx=10, pady=(10, 0))
        b = Button(self, text=button, command=self.destroy)
        b.grid(row=2, padx=10, pady=10, columnspan=2)
        self.var = BooleanVar(self)
        c = Checkbutton(self, text=checkmessage, variable=self.var)
        c.grid(row=1, padx=10, pady=4, sticky="e", columnspan=2)
        self.grab_set()
        b.focus_set()

    def get_check(self):
        return self.var.get()


def ob_checkbutton(title="", message="", button="Ok", image=None,
                   checkmessage="", **options):
    """ Open a OBCheckbutton and return the value of the checkbutton when closed. """
    ob = OBCheckbutton(title, message, button, image, checkmessage, **options)
    ob.wait_window(ob)
    return ob.get_check()
