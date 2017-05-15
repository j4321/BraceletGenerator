#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:51:34 2017

@author: juliette
"""


from tkinter import Toplevel, Tk, TclError
from tkinter.ttk import Label, Style

class Tooltip(Toplevel):
    def __init__(self, parent, **kwargs):
        Toplevel.__init__(self, parent)
        if 'title' in kwargs:
            self.title(kwargs['title'])
        self.transient(parent)
        self.attributes('-type', 'tooltip')
        self.attributes('-alpha', kwargs.get('alpha', 0.75))
        self.overrideredirect(True)
        self.configure(padx=kwargs.get('padx', 4))
        self.configure(pady=kwargs.get('pady', 4))

        self.style = Style(self)
        bg = kwargs.get('background', 'black')
        self.configure(background=bg)
        self.style.configure('tooltip.TLabel', background=bg)
        fg = kwargs.get('foreground', 'white')
        self.style.configure('tooltip.TLabel', foreground=fg)

        self.im = kwargs.get('image', None)
        self.label = Label(self, text=kwargs.get('text', ''), image=self.im,
                           style='tooltip.TLabel',
                           compound=kwargs.get('compound', 'left'))
        self.label.pack()

    def configure(self, **kwargs):
        if 'text' in kwargs:
            self.label.configure(text=kwargs.pop('text'))
        if 'image' in kwargs:
            self.label.configure(image=kwargs.pop('image'))
        if 'background' in kwargs:
            self.style.configure('tooltip.TLabel', background=kwargs['background'])
        if 'foreground' in kwargs:
            fg = kwargs.pop('foreground')
            self.style.configure('tooltip.TLabel', foreground=fg)
        if 'alpha' in kwargs:
            self.attributes('-alpha', kwargs.pop('alpha'))
        Toplevel.configure(self, **kwargs)

class TooltipWrapper:
    def __init__(self, widget, **kwargs):
        self.widget = widget
        if 'delay' in kwargs:
            self.delay = kwargs.pop('delay')
        else:
            self.delay = 1000
        self.kwargs = kwargs.copy()
        self._timer_id = None
        self.tooltip = Tooltip(self.widget, **self.kwargs)
        self.tooltip.withdraw()

        self.widget.bind('<Enter>', self._on_enter)
        self.widget.bind('<Leave>', self._on_leave)
        self.widget.bind('<FocusOut>', self._on_leave)
        self.tooltip.bind('<Leave>', self._on_leave_tooltip)

    def _on_enter(self, event):
        if not self.tooltip.winfo_ismapped():
            self._timer_id = self.widget.after(self.delay, self.display_tooltip)

    def _on_leave(self, event):
        if self.tooltip.winfo_ismapped():
            x, y = self.widget.winfo_pointerxy()
            try:
                if not self.widget.winfo_containing(x, y) in [self.widget, self.tooltip]:
                    self.tooltip.withdraw()
            except KeyError:
                self.tooltip.withdraw()
        else:
            self.widget.after_cancel(self._timer_id)

    def _on_leave_tooltip(self, event):
        x, y = self.widget.winfo_pointerxy()
        if not self.widget.winfo_containing(x, y) in [self.widget, self.tooltip]:
            self.tooltip.withdraw()

    def display_tooltip(self):
        self.tooltip.deiconify()
        x = self.widget.winfo_pointerx() + 14
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 2
        self.tooltip.geometry('+%i+%i' % (x, y))
