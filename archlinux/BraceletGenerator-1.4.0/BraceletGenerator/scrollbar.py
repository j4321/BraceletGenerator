#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scrollbar that hides automatically when not needed.
Code taken from http://effbot.org/zone/tkinter-autoscrollbar.htm
Copyright 1998 Fredrik Lundh
Copyright 2016 Juliette Monsel (adapted code to python3)
"""

from tkinter.ttk import Scrollbar
from tkinter import TclError

class AutoScrollbar(Scrollbar):
    """ a scrollbar that hides itself if it's not needed.  only
        works if you use the grid geometry manager. """

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise TclError("cannot use place with this widget")