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


Knot class for Bracelet Generator
"""

from BraceletGenerator.constantes import active_color


class Noeud:
    """ Friendship bracelet knot """
    def __init__(self, canvas, pos_x, pos_y, color_g='#FF0000', color_d='#FF0000',
                 bord_g=False, bord_d=False, deb=False, fin=False,
                 sans_noeud_deb=False, sans_noeud_fin=False):
        """ create a friendship bracelet knot for the generator
            color_g, color_d: colors of the left and right strings used to tie
            the knot.
            bord_g, bord_d: the knot is on the left / right side of the bracelet
            deb, fin: the knot is on the first / the last row of the bracelet
            sansNoeud: the knot is on the second to last row but the outmost
            string will not be used to tie a knot on the last row. """

        self.can = canvas

        # position du noeud sur le canvas
        self.x = pos_x
        self.y = pos_y

        # flèches pour indiquer le sens du noeud
        self.fleches = [[[[self.x + 6, self.y + 8,
                           self.x + 13, self.y + 15,
                           self.x + 6, self.y + 21.75 + 0.5],
                          [self.x + 6, self.y + 23.5,
                           self.x + 6, self.y + 15.5],
                          [self.x + 6, self.y + 22.5,
                           self.x + 12, self.y + 22.5]],
                         [[self.x + 20 - 6, self.y + 8,
                           self.x + 20 - 13, self.y + 15,
                           self.x + 20 - 6, self.y + 21.75 + 0.5],
                          [self.x + 20.5 - 6, self.y + 22.5 + 1,
                           self.x + 20.5 - 6, self.y + 14.5 + 1],
                          [self.x + 20.5 - 6, self.y + 22.5,
                           self.x + 20.5 - 12, self.y + 22.5]]],
                        [[[self.x + 5, self.y + 10,
                           self.x + 16, self.y + 21],
                          [self.x + 15.5, self.y + 21.5,
                           self.x + 15.5, self.y + 13.5],
                          [self.x + 15.5, self.y + 20.5,
                           self.x + 8.5, self.y + 20.5]],
                         [[self.x + 16, self.y + 10,
                           self.x + 5, self.y + 21],
                          [self.x + 5.5, self.y + 21.5,
                           self.x + 5.5, self.y + 13.5],
                          [self.x + 5.5, self.y + 20.5,
                           self.x + 11.5, self.y + 20.5]]]]

        # le noeud est-il sur un bord ?
        self.bords = dict(bord_g=bord_g, bord_d=bord_d, deb=deb, fin=fin,
                          sans_noeud_deb=sans_noeud_deb, sans_noeud_fin=sans_noeud_fin)
        # [fil entrant gauche (Gin), fil entrant droit (Din)]
        self.color = [color_g, color_d]

        # caractéristiques
        # le fil sortant de gauche est le fil entrant à droite
        self.g_out = 1
        # 0 = gauche, 1 = droit
        self.fil_noeud = 0

        # affichage
        self.fils = [self.can.create_line(self.x - 5, self.y, self.x + 10,
                                          self.y + 15, fill=self.color[0],
                                          capstyle="round", joinstyle="round",
                                          width=5),
                     self.can.create_line(self.x + 25, self.y, self.x + 10,
                                          self.y + 15, fill=self.color[1],
                                          capstyle="round", joinstyle="round",
                                          width=5),
                     self.can.create_line(self.x - 5, self.y + 30, self.x + 10,
                                          self.y + 15,
                                          capstyle="round", joinstyle="round",
                                          fill=self.color[self.g_out],
                                          width=5),
                     self.can.create_line(self.x + 25, self.y + 30,
                                          self.x + 10, self.y + 15,
                                          capstyle="round", joinstyle="round",
                                          fill=self.color[not self.g_out],
                                          width=5)]
        self.noeud = self.can.create_oval(self.x, self.y, self.x + 20,
                                          self.y + 30,
                                          fill=self.color[self.fil_noeud],
                                          activefill=active_color(self.color[self.fil_noeud]))
        self.image = [self.can.create_line(l, width=2, joinstyle="miter", tags="noeud%i" % self.noeud)
                      for l in self.fleches[self.g_out][self.fil_noeud]]
        self.can.tag_bind("noeud%i" % self.noeud, '<Enter>',
                          lambda e: self.can.itemconfigure(self.noeud, fill=active_color(self.color[self.fil_noeud])))
        self.can.tag_bind("noeud%i" % self.noeud, '<Leave>',
                          lambda e: self.can.itemconfigure(self.noeud, fill=self.color[self.fil_noeud]))

        self._bord()

    def efface(self):
        """ efface le noeud du canvas """
        for i in self.fils:
            self.can.delete(i)
        for i in self.image:
            self.can.delete(i)
        self.can.delete(self.noeud)

    def _bord(self):
        """ affiche les bords comme il faut """
        if self.bords["bord_g"]:
            if self.bords["deb"]:
                self.can.coords(self.fils[0], self.x - 5, self.y - 13,
                                self.x - 5, self.y, self.x + 10, self.y + 15)
                self.can.coords(self.fils[1], self.x + 25, self.y - 13,
                                self.x + 25, self.y, self.x + 10, self.y + 15)
            elif self.bords["sans_noeud_deb"]:
                self.can.coords(self.fils[0], self.x + 10, self.y + 15,
                                self.x - 20, self.y - 15, self.x - 5,
                                self.y - 30, self.x - 5, self.y - 43)
                self.can.coords(self.fils[1], self.x + 25, self.y,
                                self.x + 10, self.y + 15)
            else:
                self.can.coords(self.fils[0], self.x - 20, self.y - 15,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[1], self.x + 25, self.y,
                                self.x + 10, self.y + 15)

            if self.bords["fin"]:
                self.can.coords(self.fils[2], self.x - 5, self.y + 43,
                                self.x - 5, self.y + 30, self.x + 10,
                                self.y + 15)
                self.can.coords(self.fils[3], self.x + 25, self.y + 43,
                                self.x + 25, self.y + 30, self.x + 10,
                                self.y + 15)
            elif self.bords["sans_noeud_fin"]:
                self.can.coords(self.fils[2], self.x + 10, self.y + 15,
                                self.x - 20, self.y + 45, self.x - 5,
                                self.y + 60, self.x - 5, self.y + 73)
                self.can.coords(self.fils[3], self.x + 25, self.y + 30,
                                self.x + 10, self.y + 15)
            else:
                self.can.coords(self.fils[2], self.x - 20, self.y + 45,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[3], self.x + 25, self.y + 30,
                                self.x + 10, self.y + 15)

        elif self.bords["bord_d"]:
            if self.bords["deb"]:
                self.can.coords(self.fils[0], self.x - 5, self.y - 13,
                                self.x - 5, self.y, self.x + 10, self.y + 15)
                self.can.coords(self.fils[1], self.x + 25, self.y - 13,
                                self.x + 25, self.y, self.x + 10, self.y + 15)
            elif self.bords["sans_noeud_deb"]:
                self.can.coords(self.fils[0], self.x - 5, self.y,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[1], self.x + 10, self.y + 15,
                                self.x + 40, self.y - 15, self.x + 25,
                                self.y - 30, self.x + 25, self.y - 43)
            else:
                self.can.coords(self.fils[0], self.x - 5, self.y,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[1], self.x + 40, self.y - 15,
                                self.x + 10, self.y + 15)

            if self.bords["fin"]:
                self.can.coords(self.fils[2], self.x - 5, self.y + 43,
                                self.x - 5, self.y + 30, self.x + 10,
                                self.y + 15)
                self.can.coords(self.fils[3], self.x + 25, self.y + 43,
                                self.x + 25, self.y + 30, self.x + 10,
                                self.y + 15)
            elif self.bords["sans_noeud_fin"]:
                self.can.coords(self.fils[2], self.x - 5, self.y + 30,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[3], self.x + 10, self.y + 15,
                                self.x + 40, self.y + 45, self.x + 25,
                                self.y + 60, self.x + 25, self.y + 73)
            else:
                self.can.coords(self.fils[2], self.x - 5, self.y + 30,
                                self.x + 10, self.y + 15)
                self.can.coords(self.fils[3], self.x + 40, self.y + 45,
                                self.x + 10, self.y + 15)

        elif self.bords["deb"]:
            self.can.coords(self.fils[0], self.x - 5, self.y - 13, self.x - 5,
                            self.y, self.x + 10, self.y + 15)
            self.can.coords(self.fils[1], self.x + 25, self.y - 13,
                            self.x + 25, self.y, self.x + 10, self.y + 15)
            self.can.coords(self.fils[2], self.x - 5, self.y + 30,
                            self.x + 10, self.y + 15)
            self.can.coords(self.fils[3], self.x + 25, self.y + 30,
                            self.x + 10, self.y + 15)

        elif self.bords["fin"]:
            self.can.coords(self.fils[0], self.x - 5, self.y, self.x + 10,
                            self.y + 15)
            self.can.coords(self.fils[1], self.x + 25, self.y, self.x + 10,
                            self.y + 15)
            self.can.coords(self.fils[2], self.x - 5, self.y + 43, self.x - 5,
                            self.y + 30, self.x + 10, self.y + 15)
            self.can.coords(self.fils[3], self.x + 25, self.y + 43,
                            self.x + 25, self.y + 30, self.x + 10, self.y + 15)

        else:
            self.can.coords(self.fils[0], self.x - 5, self.y,
                            self.x + 10, self.y + 15)
            self.can.coords(self.fils[1], self.x + 25, self.y,
                            self.x + 10, self.y + 15)
            self.can.coords(self.fils[2], self.x - 5, self.y + 30,
                            self.x + 10, self.y + 15)
            self.can.coords(self.fils[3], self.x + 25, self.y + 30,
                            self.x + 10, self.y + 15)

    def get_color(self, fil):
        """ renvoie la color du fil
            fil: 0 = Gin, 1 = Din, 2 = Gout, 3 = Dout """
        if fil < 2:
            return self.color[fil]
        elif fil == 2:
            return self.color[self.g_out]
        else:
            return self.color[not self.g_out]

    def set_color(self, fil, color):
        """ change la color du fil 0 = Gin ou 1 = Din """
        self.color[fil] = color
        self.can.itemconfigure(self.fils[fil], fill=self.color[fil])
        self.can.itemconfigure(self.fils[2], fill=self.color[self.g_out])
        self.can.itemconfigure(self.fils[3], fill=self.color[not self.g_out])
        self.can.itemconfigure(self.noeud, fill=self.color[self.fil_noeud],
                               activefill=active_color(self.color[self.fil_noeud]))

    def get_code(self):
        """
            return the code associated with the knot for the export in text
            format:
                * forward knot = 0
                * backward knot = 1
                * backward forward = 2
                * forward backward = 3
        """
        if self.g_out == 1:
            if self.fil_noeud == 0:
                return 0
            else:
                return 1
        else:
            if self.fil_noeud == 0:
                return 3
            else:
                return 2

    def get_g_out(self):
        return self.g_out

    def get_fil_noeud(self):
        return self.fil_noeud

    def get_noeud(self):
        return self.noeud

    def get_image(self):
        """ renvoie self.image """
        return self.image

    def get_bords(self, bord):
        """ renvoie la valeur du bord passé en argument ('deb', ...) """
        return self.bords[bord]

    def set_bords(self, **bords):
        """ change la valeur des bords et actualise l'affichage du noeud
            en conséquence
            ex: set_bords(deb=True, bord_d=False)"""
        self.bords.update(bords)
        self._bord()

    def set_g_out(self, g_out):
        """ change la valeur de g_out et modifie le noeud en conséquence """
        self.g_out = g_out
        self.can.itemconfigure(self.fils[2], fill=self.color[self.g_out])
        self.can.itemconfigure(self.fils[3], fill=self.color[not self.g_out])
        for i, l in enumerate(self.fleches[self.g_out][self.fil_noeud]):
            self.can.coords(self.image[i], *l)

    def set_fil_noeud(self, fil_noeud):
        """ change la valeur de fil_noeud et modifie le noeud
            en conséquence """
        self.fil_noeud = fil_noeud
        self.can.itemconfigure(self.noeud, fill=self.color[self.fil_noeud],
                               activefill=active_color(self.color[self.fil_noeud]))
        for i, l in enumerate(self.fleches[self.g_out][self.fil_noeud]):
            self.can.coords(self.image[i], *l)

    def change_noeud(self):
        """ passe au type de noeud suivant"""
        self.fil_noeud += 1
        if self.fil_noeud == 2:
            self.fil_noeud = 0
            self.g_out += 1
            self.g_out %= 2
            self.can.itemconfigure(self.fils[2], fill=self.color[self.g_out])
            self.can.itemconfigure(self.fils[3],
                                   fill=self.color[not self.g_out])
        self.can.itemconfigure(self.noeud, fill=self.color[self.fil_noeud],
                               activefill=active_color(self.color[self.fil_noeud]))
        for i, l in enumerate(self.fleches[self.g_out][self.fil_noeud]):
            self.can.coords(self.image[i], *l)

    def change_noeud_inv(self):
        """ passe au type de noeud précédent"""
        self.fil_noeud -= 1
        if self.fil_noeud == - 1:
            self.fil_noeud = 1
            self.g_out -= 1
            self.g_out %= 2
            self.can.itemconfigure(self.fils[2], fill=self.color[self.g_out])
            self.can.itemconfigure(self.fils[3],
                                   fill=self.color[not self.g_out])
        self.can.itemconfigure(self.noeud, fill=self.color[self.fil_noeud],
                               activefill=active_color(self.color[self.fil_noeud]))
        for i, l in enumerate(self.fleches[self.g_out][self.fil_noeud]):
            self.can.coords(self.image[i], *l)
