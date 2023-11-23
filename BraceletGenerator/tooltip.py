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
along with this program.  If not, see <http: //www.gnu.org/licenses/>.


Tooltip and TooltipTreeWrapper classes to display the full path of a shortcut
when the mouse stays over long enough
"""


from tkinter import Toplevel
from tkinter.ttk import Label, Style


class Tooltip(Toplevel):
    def __init__(self, parent, **kwargs):
        Toplevel.__init__(self, parent)
        if 'title' in kwargs:
            self.title(kwargs['title'])
        self.transient(parent)
        self.attributes('-toolwindow')
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

        # delay before showing tooltip
        if 'delay' in kwargs:
            self.delay = kwargs.pop('delay')
        else:
            self.delay = 1000

        self._timer_id = None
        self.tooltip = Tooltip(self.widget, **kwargs)
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
