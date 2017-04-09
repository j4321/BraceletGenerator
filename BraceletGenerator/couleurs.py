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

Color management dialog
"""

from tkinter import Toplevel, Canvas, PhotoImage
from tkinter.ttk import Button, Label, Separator, Frame
from BraceletGenerator.constantes import BG_COLOR, MOUSEWHEEL, set_icon, mouse_wheel, fill, askcolor, LANG
from BraceletGenerator.scrollbar import AutoScrollbar as Scrollbar

class Couleurs(Toplevel):
    """ Toplevel de l'application principale permettant de gérer les colors
        utilisées """

    def __init__(self, master, coul_def, colors, **options):
        """ créer le gestionnaire de colors
            coul_def : color par défaut,
            colors : set des colors du bracelet
        """
        # Initialisation Toplevel
        Toplevel.__init__(self, master, **options)
        self.title(_("Color Manager"))
        self.resizable(0,1)
        self.transient(master)
        self.grab_set()
        self.configure(bg=BG_COLOR)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.protocol("WM_DELETE_WINDOW", self._quitter)

        g, x, y = self.master.geometry().split("+")
        self.geometry("+%s+%s" % (x,y))

        # Résultats (nouvelles colors)
        self.result = ()

        # Icône
        set_icon(self)

        ### Contenu :
        self.can = Canvas(self,bg=BG_COLOR) # pour utiliser une scrollbar
        self.can.grid(row=0, column=0, sticky="nswe")

        self.scroll_vert = Scrollbar(self, command=self.can.yview,
                                     orient="vertical")

        self.can.configure(yscrollcommand=self.scroll_vert.set)

        self.scroll_vert.grid(row=0, column=1, sticky="ns")
        self.is_scrollable = True

        fen = Frame(self)
        self.can.create_window(0, 0, window=fen, anchor="nw")

        ### Couleur par défaut
        Label(fen, text=_("Default color")).grid(row=2, column=0, padx=6,
                                                 sticky="e")
        self.current_default = PhotoImage(master=self, width=16, height=16)
        fill(self.current_default, coul_def)
        Label(fen, image=self.current_default).grid(row=2, column=1, padx=6)
        self.b_new_default = Button(fen, command=lambda : self.change_color(self.b_new_default))
        self.b_new_default.image = PhotoImage(master=self, width=16, height=16)
        self.b_new_default.configure(image=self.b_new_default.image)
        fill(self.b_new_default.image, coul_def)
        self.b_new_default.grid(row=2, column=2, padx=6, pady=4)

        Separator(fen, orient="horizontal").grid(row=3, column=0, pady=4,
                                                  columnspan=3, sticky="ew")
        ### Couleurs des fils
        Label(fen, text=_("String colors")).grid(row=4, column=0, padx=6,
                                                 sticky="e")
        self.current_colors = []
        self.b_new_colors = []
        for i,coul in enumerate(colors):
            self.current_colors.append(PhotoImage(master=self, width=16, height=16))
            fill(self.current_colors[i], coul)
            Label(fen, image=self.current_colors[i]).grid(row=4+i, column=1, padx=6)
            self.b_new_colors.append(Button(fen))
            self.b_new_colors[i].image = PhotoImage(master=self, width=16, height=16)
            fill(self.b_new_colors[i].image, coul)
            self.b_new_colors[i].configure(image=self.b_new_colors[i].image,
                                           command=lambda b=self.b_new_colors[i]: self.change_color(b))
            self.b_new_colors[i].grid(row=4+i, column=2, padx=6, pady=4)

        Button(fen, text="Ok",
               command=self.valide).grid(row=5+len(colors), pady=4,
                                         column=0, columnspan=3)
        self.update()
        bbox = self.can.bbox("all")
        self.can.configure(width=bbox[2], height=min(self.winfo_screenheight() - 180, bbox[3]), scrollregion=bbox)

        # mouse scroll
        for key in MOUSEWHEEL:
            self.can.bind_all(key, self._mouse_scroll)

    def _mouse_scroll(self, event):
        """ utilisation de la molette de la souris pour faire défiler
            verticalement le canvas """
        if self.is_scrollable:
            self.can.yview_scroll(mouse_wheel(event), "units")

    def change_color(self, button):
        image = button.image
        c_coul = "#%02x%02x%02x" % image.get(0,0)
        n_coul = askcolor(c_coul, master=self)
        if n_coul:
            fill(image, n_coul)
            # otherwise the image is not refreshed in windows unless the button takes focus
            button.configure(image=image)

    def valide(self):
        coul_def = "#%02x%02x%02x" % self.b_new_default.image.get(0,0)
        colors = ["#%02x%02x%02x" % b.image.get(0,0) for b in self.b_new_colors]
        self.result = (coul_def, colors)
        self.destroy()

    def _quitter(self):
        self.destroy()

    def get_result(self):
        return self.result
