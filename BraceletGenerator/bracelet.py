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


bracelet class for Bracelet Generator
"""


import os
from pickle import Pickler, Unpickler
from PIL import Image
from tkinter import Tk, Menu, StringVar, Canvas
from tkinter.ttk import Button, Label, Style, Frame, Entry
from tkinter.messagebox import showerror, showinfo
from tkinter.messagebox import askyesnocancel
from BraceletGenerator.scrollbar import AutoScrollbar as Scrollbar
import BraceletGenerator.constantes as cst
from BraceletGenerator.noeud import Noeud
from BraceletGenerator.couleurs import Couleurs
from BraceletGenerator.bicolore import Bicolore
from BraceletGenerator.tooltip import TooltipWrapper
from BraceletGenerator.about import About
from BraceletGenerator.version_check import UpdateChecker


class Bracelet(Tk):
    """ patron de bracelet brésilien """

    def __init__(self, row_nb=4, string_nb=4, color="#ff0000", fichier=""):
        """ fichier: chemin du fichier où sont sauvegardées les données
            du patron """
        # root window
        Tk.__init__(self, className="BraceletGenerator")
        self.title(_("Bracelet Generator"))
        self.config(bg=cst.BG_COLOR)
        cst.set_icon(self)
        self.minsize(330, 295)
        self.maxsize(width=self.winfo_screenwidth(),
                     height=self.winfo_screenheight())
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        # fonction de validation des entrées
        self._okfct = self.register(cst.valide_entree_nb)

        # --- style
        self.style = Style(self)
        self.style.theme_use(cst.STYLE)
        self.style.configure('TButton', background=cst.BG_COLOR)
        self.style.configure('pm.TButton', padding=1)
        self.style.configure('TCheckbutton', background=cst.BG_COLOR)
        self.style.configure('TLabel', background=cst.BG_COLOR)
        self.style.configure('TFrame', background=cst.BG_COLOR)
        self.style.configure('flat.TButton', relief="flat", padding=2,
                             background=cst.BG_COLOR)
        self.style.map('flat.TButton',
                       background=[("disabled", cst.BG_COLOR),
                                   ("active", "!disabled",
                                    self.style.lookup("TButton", "background",
                                                      state=("active", "!disabled")))])
        self.style.configure("test.TButton", padding=2)

        # --- menu
        # --- -- icônes
        self.m_plus = cst.open_image(file=cst.IM_PLUS_M, master=self)
        self.m_moins = cst.open_image(file=cst.IM_MOINS_M, master=self)
        self.m_exit = cst.open_image(master=self, file=cst.IM_EXIT_M)
        self.m_export = cst.open_image(master=self, file=cst.IM_EXPORT_M)
        self.m_export_txt = cst.open_image(master=self, file=cst.IM_EXPORT_TXT_M)
        self.m_new = cst.open_image(master=self, file=cst.IM_NEW_M)
        self.m_open = cst.open_image(master=self, file=cst.IM_OUVRIR_M)
        self.m_saveas = cst.open_image(master=self, file=cst.IM_SAVEAS_M)
        self.m_sauve = cst.open_image(master=self, file=cst.IM_SAUVER_M)
        self.m_undo = cst.open_image(master=self, file=cst.IM_UNDO)
        self.m_redo = cst.open_image(master=self, file=cst.IM_REDO)
        self.m_bicolore = cst.open_image(master=self, file=cst.IM_BICOLORE_M)
        self.m_help = cst.open_image(master=self, file=cst.IM_AIDE)
        self.m_about = cst.open_image(master=self, file=cst.IM_ABOUT)
        self.m_sym_horizontal = cst.open_image(master=self, file=cst.IM_SYM_HORIZ_M)
        self.m_sym_vertical = cst.open_image(master=self, file=cst.IM_SYM_VERT_M)
        self.m_color = cst.open_image(master=self, file=cst.IM_COLOR_M)

        # barre de menus
        menu = Menu(self, tearoff=0, borderwidth=0,
                    bg=cst.BG_COLOR, activeborder=0)
        # --- -- Fichier
        self.menu_file = Menu(menu, tearoff=0, bg=cst.BG_COLOR)
        self.menu_recent_files = Menu(self.menu_file, tearoff=0, bg=cst.BG_COLOR)
        self.menu_file.add_command(label=_("New"), image=self.m_new,
                                   compound="left", command=self.new,
                                   accelerator='Ctrl+N')
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Open"), image=self.m_open,
                                   compound="left", command=self.open,
                                   accelerator='Ctrl+O')
        self.menu_file.add_cascade(label=_("Recent Files"),
                                   image=self.m_open,
                                   compound="left",
                                   menu=self.menu_recent_files)
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Save"), image=self.m_sauve,
                                   compound="left", command=self.save,
                                   accelerator='Ctrl+S')
        self.menu_file.add_command(label=_("Save As"), image=self.m_saveas,
                                   compound="left", command=self.saveas,
                                   accelerator=_("Shift+Ctrl+S"))
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Export as picture"), image=self.m_export,
                                   compound="left", command=self.export,
                                   accelerator="Ctrl+E")
        self.menu_file.add_command(label=_("Export as text"), image=self.m_export_txt,
                                   compound="left", command=self.export_txt,
                                   accelerator="Shift+Ctrl+E")
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Quit"), image=self.m_exit,
                                   compound="left", command=self.exit,
                                   accelerator="Ctrl+Q")
        if cst.RECENT_FILES:
            for file in cst.RECENT_FILES:
                self.menu_recent_files.add_command(label=file,
                                                   command=lambda fichier=file: self.open(fichier=fichier))
        else:
            self.menu_file.entryconfigure(3, state="disabled")

        # --- -- Édition
        self.menu_edit = Menu(menu, tearoff=0, bg=cst.BG_COLOR)
        self.menu_edit.add_command(label=_("Undo"), image=self.m_undo,
                                   compound="left", command=self.undo,
                                   accelerator="Ctrl+Z")
        self.menu_edit.add_command(label=_("Redo"), image=self.m_redo,
                                   compound="left", command=self.redo,
                                   accelerator="Ctrl+Y")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Add Row"),
                                   image=self.m_plus,
                                   compound="left",
                                   command=self.add_row,
                                   accelerator="+")
        self.menu_edit.add_command(label=_("Delete Row"),
                                   image=self.m_moins,
                                   compound="left",
                                   command=self.del_row,
                                   accelerator="-")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Add String"),
                                   image=self.m_plus,
                                   compound="left",
                                   command=self.add_string,
                                   accelerator="Ctrl++")
        self.menu_edit.add_command(label=_("Delete String"),
                                   image=self.m_moins,
                                   compound="left",
                                   command=self.del_string,
                                   accelerator="Ctrl+-")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Create a Two-Colored Motif"),
                                   image=self.m_bicolore, compound="left",
                                   command=self.bicolore,
                                   accelerator="Ctrl+B")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Vertical Symmetry"),
                                   image=self.m_sym_vertical, compound="left",
                                   command=lambda: self.symmetrize("vertical"),
                                   accelerator="Ctrl+V")
        self.menu_edit.add_command(label=_("Horizontal Symmetry"),
                                   image=self.m_sym_horizontal, compound="left",
                                   command=lambda: self.symmetrize("horizontal"),
                                   accelerator="Ctrl+H")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Color Manager"),
                                   image=self.m_color, compound="left",
                                   command=self.manage_colors,
                                   accelerator="Ctrl+C")
        # --- -- Langue
        self.menu_language = Menu(menu, tearoff=0, bg=cst.BG_COLOR)
        self.langue = StringVar(self)
        self.langue.set(cst.LANGUE[:2])
        self.menu_language.add_radiobutton(label="Français",
                                           variable=self.langue,
                                           value="fr", command=self._translate)
        self.menu_language.add_radiobutton(label="English", variable=self.langue,
                                           value="en", command=self._translate)
        # --- -- Aide
        self.menu_help = Menu(menu, tearoff=0, bg=cst.BG_COLOR)
        self.menu_help.add_command(label=_("Help"), image=self.m_help, command=cst.help,
                                   compound="left", accelerator="F1")
        self.menu_help.add_command(label=_("Online Help"), image=self.m_help,
                                   command=cst.help_web, compound="left",
                                   accelerator="Ctrl+F1")
        self.menu_help.add_separator()
        self.menu_help.add_command(label=_("Check for updates"),
                                   command=lambda: UpdateChecker(self))
        self.menu_help.add_separator()
        self.menu_help.add_command(label=_("About"), image=self.m_about,
                                   command=self.about, compound="left")

        # --- -- Ajout des menus à la barre
        menu.add_cascade(label=_("File"), menu=self.menu_file)
        menu.add_cascade(label=_("Edit"), menu=self.menu_edit)
        menu.add_cascade(label=_("Language"), menu=self.menu_language)
        menu.add_cascade(label=_("Help"), menu=self.menu_help)
        # affichage de la barre de menu
        self.config(menu=menu)

        # --- toolbar
        toolbar = Frame(self, height=24)
        toolbar.grid(row=0, sticky="wn")
        self.icon_exit = cst.open_image(master=self, file=cst.IM_EXIT)
        self.icon_export = cst.open_image(master=self, file=cst.IM_EXPORT)
        self.icon_new = cst.open_image(master=self, file=cst.IM_NEW)
        self.icon_open = cst.open_image(master=self, file=cst.IM_OUVRIR)
        self.icon_save = cst.open_image(master=self, file=cst.IM_SAUVER)
        self.icon_bicolore = cst.open_image(master=self, file=cst.IM_BICOLORE)
        self.icon_sym_horiz = cst.open_image(master=self, file=cst.IM_SYM_HORIZ)
        self.icon_sym_vert = cst.open_image(master=self, file=cst.IM_SYM_VERT)
        self.icon_color = cst.open_image(master=self, file=cst.IM_COLOR)
        b_new = Button(toolbar, image=self.icon_new, command=self.new,
                       style='flat.TButton')
        TooltipWrapper(b_new, text=_("New"))
        b_new.grid(column=0, row=0)
        b_open = Button(toolbar, image=self.icon_open, command=self.open,
                        style='flat.TButton')
        TooltipWrapper(b_open, text=_("Open"))
        b_open.grid(column=1, row=0)
        self.save_button = Button(toolbar, image=self.icon_save,
                                  command=self.save,
                                  style='flat.TButton')
        TooltipWrapper(self.save_button, text=_("Save"))
        self.save_button.grid(column=2, row=0)
        b_export = Button(toolbar, image=self.icon_export, command=self.export,
                          style='flat.TButton')
        TooltipWrapper(b_export, text=_("Export as picture"))
        b_export.grid(column=3, row=0)
        b_bic = Button(toolbar, image=self.icon_bicolore,
                       command=self.bicolore, style='flat.TButton')
        TooltipWrapper(b_bic, text=_("Open two-colored motif editor"))
        b_bic.grid(column=4, row=0)
        b_sym_v = Button(toolbar, image=self.icon_sym_vert,
                         command=lambda: self.symmetrize("vertical"),
                         style='flat.TButton')
        TooltipWrapper(b_sym_v, text=_("Vertical Symmetry"))
        b_sym_v.grid(column=5, row=0)
        b_sym_h = Button(toolbar, image=self.icon_sym_horiz,
                         command=lambda: self.symmetrize("horizontal"),
                         style='flat.TButton')
        TooltipWrapper(b_sym_h, text=_("Horizontal Symmetry"))
        b_sym_h.grid(column=6, row=0)

        b_color = Button(toolbar, style='flat.TButton', image=self.icon_color,
                         command=self.manage_colors)
        TooltipWrapper(b_color, text=_("Open color manager"))
        b_color.grid(row=0, column=7)
        b_quit = Button(toolbar, image=self.icon_exit, command=self.exit,
                        style='flat.TButton')
        TooltipWrapper(b_quit, text=_("Quit"))
        b_quit.grid(column=8, row=0)

        # --- frame contenant le patron
        pattern_frame = Frame(self, relief="sunken", borderwidth=1)
        pattern_frame.grid(row=1, sticky="nwes")

        # --- toolbar2
        toolbar2 = Frame(pattern_frame, height=24)
        toolbar2.grid(row=0, column=0, sticky="ew", pady=(8, 4))
        self.icon_plus = cst.open_image(master=self, file=cst.IM_PLUS)
        self.icon_moins = cst.open_image(master=self, file=cst.IM_MOINS)

        Label(toolbar2, text=_("Rows: ")).grid(row=0, column=0,
                                               sticky="e", padx=(5, 0))
        self.row_nb_entry = Entry(toolbar2, width=3,
                                  validatecommand=(self._okfct, '%d', '%S'),
                                  validate='key', justify="center")
        self.row_nb_entry.grid(row=0, column=1, sticky="nsw", padx=(0, 5))
        b_pl = Button(toolbar2, image=self.icon_plus, style="pm.TButton",
                      command=self.add_row)
        TooltipWrapper(b_pl, text=_("Add Row"))
        b_pl.grid(row=0, column=2, padx=2, sticky="ewsn")
        b_ml = Button(toolbar2, image=self.icon_moins, style="pm.TButton",
                      command=self.del_row)
        TooltipWrapper(b_ml, text=_("Delete Row"))
        b_ml.grid(row=0, column=3, padx=2, sticky="ewsn")
        Label(toolbar2, text=_("Strings: ")).grid(row=0, column=4,
                                                  sticky="e", padx=(5, 0))
        self.string_nb_entry = Entry(toolbar2, width=3,
                                     validatecommand=(self._okfct, '%d', '%S'),
                                     validate='key', justify="center")
        self.string_nb_entry.grid(row=0, column=5, sticky="ens", padx=(0, 5))
        b_pf = Button(toolbar2, image=self.icon_plus, style="pm.TButton",
                      command=self.add_string)
        TooltipWrapper(b_pf, text=_("Add String"))
        b_pf.grid(row=0, column=6, padx=2)
        b_mf = Button(toolbar2, image=self.icon_moins, style="pm.TButton",
                      command=self.del_string)
        TooltipWrapper(b_mf, text=_("Delete String"))
        b_mf.grid(row=0, column=7, padx=2)

        # --- propriétés du bracelet
        # color par défaut
        self.color = color
        # le nombre de lignes est toujours pair
        self.row_nb = (row_nb // 2) * 2
        self.string_nb = string_nb
        # savoir si l'éditeur de motifs bicolores est ouvert
        self.bicolore_on = False

        # --- canvas
        self.height_max = pattern_frame.winfo_screenheight() - 180
        self.width_max = pattern_frame.winfo_screenwidth() - 50

        self.can = Canvas(pattern_frame, borderwidth=2, relief="groove",
                          bg=cst.CANVAS_COLOR)
        self.can.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)

        self.scroll_vert = Scrollbar(pattern_frame, command=self.can.yview,
                                     orient="vertical")
        self.scroll_horiz = Scrollbar(pattern_frame, command=self.can.xview,
                                      orient="horizontal")

        self.can.configure(yscrollcommand=self.scroll_vert.set)
        self.can.configure(xscrollcommand=self.scroll_horiz.set)

        pattern_frame.rowconfigure(1, weight=1)
        pattern_frame.columnconfigure(0, weight=1)

        self.scroll_vert.grid(row=1, column=1, sticky="ns")
        self.scroll_horiz.grid(row=2, column=0, sticky="ew")

        # --- Raccourcis clavier
        self.bind('<Control-o>', self.open)
        self.bind('<Control-n>', self.new)
        self.bind('<Control-s>', self.save)
        self.bind('<Control-Shift-S>', self.saveas)
        self.bind('<Control-e>', self.export)
        self.bind('<Control-Shift-E>', self.export_txt)
        self.bind('<Control-q>', self.exit)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-y>', self.redo)
        self.bind('<Control-b>', self.bicolore)
        self.bind('<Control-c>', self.manage_colors)
        self.bind('<Key-F1>', help)
        self.bind('<Control-Key-F1>', cst.help_web)
        self.bind('<Control-h>', lambda event: self.symmetrize("horizontal"))
        self.bind('<Control-v>', lambda event: self.symmetrize("vertical"))
        self.bind("<KP_Add>", self.add_row)
        self.bind("<KP_Subtract>", self.del_row)
        self.bind("<Control-KP_Add>", self.add_string)
        self.bind("<Control-KP_Subtract>", self.del_string)
        self.bind("<plus>", self.add_row)
        self.bind("<minus>", self.del_row)
        self.bind("<Control-plus>", self.add_string)
        self.bind("<Control-minus>", self.del_string)
        self.row_nb_entry.bind("<Return>", self.change_row_nb)
        self.row_nb_entry.bind("<FocusOut>", self.change_row_nb)
        self.string_nb_entry.bind("<Return>", self.change_string_nb)
        self.string_nb_entry.bind("<FocusOut>", self.change_string_nb)

        # faire défiler le canvas à l'aide de la molette de la souris
        for key in cst.MOUSEWHEEL:
            self.bind(key, self._mouse_scroll)
        self.can.bind("<Configure>", self._on_configure)

        self.path_save = fichier

        # --- Initialisation
        self.init_canvas()
        self.is_saved = True
        self._logreinit()

        if fichier:
            self.open(fichier=fichier)
        else:
            self.path_save = ""  # saved pattern path

        # --- Update check
        if cst.CONFIG.getboolean("General", "check_update"):
            UpdateChecker(self)

    def _on_configure(self, event):
        h = self.can.winfo_height()
        bbox = self.can.bbox("all")

        if h > bbox[3] - bbox[1] + 20:
            y2 = bbox[1] - 16 + h
        else:
            y2 = bbox[3] + 10
        self.can.configure(scrollregion=[bbox[0] - 10,
                                         bbox[1] - 10,
                                         bbox[2] + 10,
                                         y2])

    def __setattr__(self, name, value):
        """ gestion de la modification attributs, en particulier
            les nombres de fils et de lignes ainsi que la sauvegarde """
        if name == "string_nb":
            self.string_nb_entry.delete(0, "end")
            self.string_nb_entry.insert(0, value)
        elif name == "row_nb":
            self.row_nb_entry.delete(0, "end")
            self.row_nb_entry.insert(0, value)
        elif name == "is_saved":
            dico = {"True": "disabled", "False": "normal"}
            self.save_button.configure(state=dico[str(value)])
            self.menu_file.entryconfigure(5, state=dico[str(value)])
        elif name == "path_save":
            if not value:
                self.save_button.configure(state="disabled")
                self.menu_file.entryconfigure(5, state="disabled")

        object.__setattr__(self, name, value)

    def _mouse_scroll(self, event):
        """ utilisation de la molette de la souris pour faire défiler
            verticalement le canvas """
        self.can.yview_scroll(cst.mouse_wheel(event), "units")

    def _attribue_carre(self, i):
        """ astuce pour réaliser les tag_bind dans une boucle """
        self.can.tag_bind(self.colors[i], '<Button-1>',
                          lambda event: self._clic_carre(i))

    def _attribue_noeud(self, i, j):
        """ astuce pour réaliser les tag_bind dans une boucle """
        self.can.tag_bind(self.noeuds[i][j].get_noeud(), '<Button-1>',
                          lambda event: self._clic_noeud(i, j))
        self.can.tag_bind(self.noeuds[i][j].get_noeud(), cst.RIGHT_CLICK,
                          lambda event: self._clic_noeud_inv(i, j))
        im = self.noeuds[i][j].get_image()
        for l in im:
            self.can.tag_bind(l, '<Button-1>',
                              lambda event: self._clic_noeud(i, j))
            self.can.tag_bind(l, cst.RIGHT_CLICK,
                              lambda event: self._clic_noeud_inv(i, j))

    def init_canvas(self):
        """ (ré)initialisation du canvas et des variables associées,
            affichage des noeuds ... """
        self.can.delete("all")
        # largeur sur le canvas du patron interactif
        self.fin_noeud = 50 + (self.string_nb // 2) * 60 + 30 * (self.string_nb % 2)
        # noeuds du bracelets
        self.noeuds = []
        # carrés de sélection de la couleur des fils
        self.colors = []
        # numéros des fils
        self.string_numbers = []
        # numéros des rangs
        self.row_numbers = []
        # carreaux affichant le motif à droite du patron
        self.motif = []
        for i in range(self.row_nb * 4):
            self.motif.append([])
        # info sur la couleur des fils de gauche et de droite de chaque
        # noeud du 2e quart
        self.motif2 = []
        # info sur la couleur des fils de gauche et de droite de chaque
        # noeud du 3e quart
        self.motif3 = []
        w = self.fin_noeud + 28 + (self.string_nb // 2) * 16 + (self.string_nb % 2) * 8
        self.can.configure(width=min(self.width_max, max(w + 20, 230)),
                           height=min(30 + (self.row_nb + 2) * 30, self.height_max))

        # création des carrés pour sélectionner la couleur des fils
        for i in range(self.string_nb):
            self.string_numbers.append(self.can.create_text(45 + 30 * i, 9,
                                                            text="%i" % (i + 1),
                                                            anchor="s",
                                                            font=("Arial", '12')))
            self.colors.append(self.can.create_rectangle(41 + 30 * i, 13,
                                                         49 + 30 * i, 21,
                                                         fill=self.color,
                                                         activefill=cst.active_color(self.color)))
            self._attribue_carre(i)

        # création des noeuds et des carreaux du motif
        for i in range(self.row_nb):
            self.noeuds.append([])
            self.motif2.append([])
            self.motif3.append([])
            if i % 2:  # ligne impaire
                self.row_numbers.append(self.can.create_text(10, 25 + (i + 1) * 30,
                                                             text="%i" % (i + 1),
                                                             anchor="e",
                                                             font=("Arial", '12')))
                nb_noeuds = self.string_nb // 2 - 1 + self.string_nb % 2
                for j in range(nb_noeuds):
                    self.noeuds[i].append(Noeud(self.can, 80 + j * 60,
                                                10 + (i + 1) * 30,
                                                color_d=self.color,
                                                color_g=self.color))
                    self._attribue_noeud(i, j)
                    self.motif[i].append(self._carreau(self.fin_noeud + 28 + j * 16, 28 + i // 2 * 16))
                    self.motif[i + self.row_nb].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                                     28 + (i + self.row_nb) // 2 * 16))
                    self.motif[i + 2 * self.row_nb].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                                         28 + (i + 2 * self.row_nb) // 2 * 16))
                    self.motif[i + 3 * self.row_nb].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                                         28 + (i + 3 * self.row_nb) // 2 * 16))
                    self.motif2[i].append([self.color, self.color])
                    self.motif3[i].append([self.color, self.color])
            else:  # ligne paire
                nb_noeuds = self.string_nb // 2
                for j in range(nb_noeuds):
                    self.noeuds[i].append(Noeud(self.can, 50 + j * 60,
                                                10 + (i + 1) * 30,
                                                color_d=self.color,
                                                color_g=self.color))
                    self._attribue_noeud(i, j)
                    self.motif[i].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                       20 + i // 2 * 16))
                    self.motif[i + self.row_nb].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                                     20 + (i + self.row_nb) // 2 * 16))
                    self.motif[i + 2 * self.row_nb].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                                         20 + (i + 2 * self.row_nb) // 2 * 16))
                    self.motif[i + 3 * self.row_nb].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                                         20 + (i + 3 * self.row_nb) // 2 * 16))
                    self.motif2[i].append([self.color, self.color])
                    self.motif3[i].append([self.color, self.color])
        # gestion des bords
        for noeud in self.noeuds[0]:
            noeud.set_bords(deb=True)
        for i in range(0, self.row_nb, 2):
            self.noeuds[i][0].set_bords(bord_g=True)
        for i in range(self.string_nb % 2, self.row_nb, 2):
            self.noeuds[i][-1].set_bords(bord_d=True)
        for noeud in self.noeuds[-1]:
            noeud.set_bords(fin=True)
        self.noeuds[-2][0].set_bords(sans_noeud_fin=True)
        if self.string_nb % 2:
            self.noeuds[1][-1].set_bords(sans_noeud_deb=True)
        else:
            self.noeuds[-2][-1].set_bords(sans_noeud_fin=True)

        bbox = self.can.bbox("all")
        self.can.configure(scrollregion=[bbox[0] - 10,
                                         bbox[1] - 10,
                                         bbox[2] + 10,
                                         bbox[3] + 10])

    def _carreau(self, x, y):
        """ dessine un _carreau de centre (x, y) et de 'rayon' r sur le canvas 2
            renvoie l'id du _carreau """
        return self.can.create_polygon(x, y - 8, x + 8, y, x, y + 8, x - 8, y,
                                       fill=self.color, outline='black')

    def _translate_carreau(self, i, j, x_c, y_c):
        """ translate le carreau (i, j) de façon à ce que son centre ait
            pour coordonnées (x_c, y_c) """
        self.can.coords(self.motif[i][j], x_c, y_c - 8, x_c + 8, y_c, x_c,
                        y_c + 8, x_c - 8, y_c)

    def _clic_noeud(self, i, j, write_log=True):
        """ action déclenchée par un clic gauche de la souris sur le
            noeud (i, j)"""
        self.focus_set()
        if write_log:
            self._log()
            with open(cst.BRACELET_LOG, "a") as log:
                log.write("clic_noeud %i %i\n" % (i, j))

        n = self.noeuds[i][j]
        n.change_noeud()
        self._change_color(i, j, 0, n.get_color(0))
        self._change_color(i, j, 1, n.get_color(1))
        self._actualise_motif()
        self.is_saved = False

    def _clic_noeud_inv(self, i, j, write_log=True):
        """ action déclenchée par un clic droit de la souris sur le
            noeud (i, j)"""
        self.focus_set()
        if write_log:
            self._log()
            with open(cst.BRACELET_LOG, "a") as log:
                log.write("clic_noeud_inv %i %i\n" % (i, j))

        n = self.noeuds[i][j]
        n.change_noeud_inv()
        self._change_color(i, j, 0, n.get_color(0))
        self._change_color(i, j, 1, n.get_color(1))
        self._actualise_motif()
        self.is_saved = False

    def _clic_carre(self, j):
        """ actio déclenchée par le clic sur un carré: sélection de
            la couleur du fil """
        self.focus_set()
        self._select_color(j)
        self.is_saved = False

    def _select_color(self, j, write_log=True, color=None):
        """ choix de la couleur du fil j """
        coul0 = self.can.itemcget(self.colors[j], "fill")
        if color is None:
            color = cst.askcolor(coul0, parent=self)  # color choisie en hexadécimal
        if color:
            if write_log:
                self._log()
                with open(cst.BRACELET_LOG, "a") as log:
                    log.write("change_color %i %s %s\n" % (j, coul0, color))

            self.can.itemconfigure(self.colors[j], fill=color,
                                   activefill=cst.active_color(color))
            if j < self.string_nb - 1 or j % 2:
                self._change_color(0, j // 2, j % 2, color)
            else:
                # le dernier fil ne sert pas à faire de noeud sur la
                # première ligne
                self._change_color(1, j // 2 - 1, 1, color)
            self._actualise_motif()

    def _change_color(self, i, j, fil, color):
        """ change la couleur du fil entrant gauche (0) ou droit (1)
            du noeud (i, j) et actualise les suivants """
        if i < self.row_nb:
            n = self.noeuds[i][j]
            n.set_color(fil, color)
            if n.get_fil_noeud() == fil:
                self.can.itemconfig(self.motif[i][j], fill=color)
            if fil:
                sortie = not n.g_out
            else:
                sortie = n.g_out
            if i < self.row_nb - 1:
                if i % 2:
                    j2 = j + sortie
                    if (j2 < len(self.noeuds[i])) or (not self.string_nb % 2):
                        self._change_color(i + 1, j2, not sortie, color)
                    elif not n.get_bords("sans_noeud_fin"):
                        self._change_color(i + 2, j, 1, color)
                else:
                    j2 = j - 1 + sortie
                    if j2 >= 0 and j2 < len(self.noeuds[i + 1]):
                        self._change_color(i + 1, j2, not sortie, color)
                    elif not n.get_bords("sans_noeud_fin"):
                        self._change_color(i + 2, j, sortie, color)

    def _change_color_virtuel(self, i, j, fil, color, motif):
        """ change la couleur du fil entrant gauche (0) ou droit (1) du
            noeud (i, j) et actualise les suivants de manière virtuelle :
            ne change que la couleur des _carreaux de self.motif
            motif = 1, 2 ou 3 indique s'il s'agit du 2e, 3e ou 4e quart
            du motif que l'on change """
        if i < self.row_nb:
            n = self.noeuds[i][j]
            if motif == 1:
                self.motif2[i][j][fil] = color
            elif motif == 2:
                self.motif3[i][j][fil] = color
            if fil == n.get_fil_noeud():
                self.can.itemconfig(self.motif[i + self.row_nb * motif][j],
                                    fill=color)
            if fil:
                sortie = not n.g_out
            else:
                sortie = n.g_out
            if i < self.row_nb - 1:
                if i % 2:
                    j2 = j + sortie
                    if (j2 < len(self.noeuds[i])) or (not self.string_nb % 2):
                        self._change_color_virtuel(i + 1, j2, not sortie,
                                                   color, motif)
                    elif not n.get_bords("sans_noeud_fin"):
                        self._change_color_virtuel(i + 2, j, 1, color, motif)
                else:
                    j2 = j - 1 + sortie
                    if j2 >= 0 and j2 < len(self.noeuds[i + 1]):
                        self._change_color_virtuel(i + 1, j2, not sortie,
                                                   color, motif)
                    elif not n.get_bords("sans_noeud_fin"):
                        self._change_color_virtuel(i + 2, j, sortie,
                                                   color, motif)

    def _actualise_motif(self):
        """ met à jour le motif en répercutant les changement de noeuds
            sur tous les rangs suivants """
        nb = len(self.noeuds[0])

        # --- 2e quart du motif
        # extrémités
        n = self.noeuds[-2][0]
        self._change_color_virtuel(0, 0, 0, n.get_color(n.get_g_out()), 1)
        if self.string_nb % 2 == 0:
            n = self.noeuds[-2][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       n.get_color(not n.get_g_out()), 1)
            # les autres noeuds
            for j, n in enumerate(self.noeuds[-1]):
                self._change_color_virtuel(0, j, 1,
                                           n.get_color(n.get_g_out()), 1)
                self._change_color_virtuel(0, j + 1, 0,
                                           n.get_color(not n.get_g_out()), 1)
        else:
            n = self.noeuds[-1][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       n.get_color(n.get_g_out()), 1)
            self._change_color_virtuel(1, nb - 1, 1,
                                       n.get_color(not n.get_g_out()), 1)
            for j, n in list(enumerate(self.noeuds[-1]))[:-1]:
                self._change_color_virtuel(0, j, 1,
                                           n.get_color(n.get_g_out()), 1)
                self._change_color_virtuel(0, j + 1, 0,
                                           n.get_color(not n.get_g_out()), 1)
        # --- 3e quart du motif
        # extrémités
        n = self.noeuds[-2][0]
        self._change_color_virtuel(0, 0, 0, self.motif2[-2][0][n.get_g_out()], 2)
        if self.string_nb % 2 == 0:
            n = self.noeuds[-2][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       self.motif2[-2][-1][not n.get_g_out()], 2)
            # les autres noeuds
            for j, n in enumerate(self.noeuds[-1]):
                self._change_color_virtuel(0, j, 1,
                                           self.motif2[-1][j][n.get_g_out()], 2)
                self._change_color_virtuel(0, j + 1, 0,
                                           self.motif2[-1][j][not n.get_g_out()], 2)
        else:
            n = self.noeuds[-1][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       self.motif2[-1][-1][n.get_g_out()], 2)
            self._change_color_virtuel(1, nb - 1, 1,
                                       self.motif2[-1][-1][not n.get_g_out()], 2)

            for j, n in list(enumerate(self.noeuds[-1]))[:-1]:
                self._change_color_virtuel(0, j, 1,
                                           self.motif2[-1][j][n.get_g_out()], 2)
                self._change_color_virtuel(0, j + 1, 0,
                                           self.motif2[-1][j][not n.get_g_out()], 2)
        # --- 4e quart du motif
        # extrémités
        n = self.noeuds[-2][0]
        self._change_color_virtuel(0, 0, 0, self.motif3[-2][0][n.get_g_out()], 3)
        if self.string_nb % 2 == 0:
            n = self.noeuds[-2][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       self.motif3[-2][-1][not n.get_g_out()], 3)
            # les autres noeuds
            for j, n in enumerate(self.noeuds[-1]):
                self._change_color_virtuel(0, j, 1,
                                           self.motif3[-1][j][n.get_g_out()], 3)
                self._change_color_virtuel(0, j + 1, 0,
                                           self.motif3[-1][j][not n.get_g_out()], 3)
        else:
            n = self.noeuds[-1][-1]
            self._change_color_virtuel(0, nb - 1, 1,
                                       self.motif3[-1][-1][n.get_g_out()], 3)
            self._change_color_virtuel(1, nb - 1, 1,
                                       self.motif3[-1][-1][not n.get_g_out()], 3)
            for j, n in list(enumerate(self.noeuds[-1]))[:-1]:
                self._change_color_virtuel(0, j, 1,
                                           self.motif3[-1][j][n.get_g_out()], 3)
                self._change_color_virtuel(0, j + 1, 0,
                                           self.motif3[-1][j][not n.get_g_out()], 3)

    def change_row_nb(self, event=None):
        ch = self.row_nb_entry.get()
        if ch:
            nb = int(ch)
            if nb >= 2:
                diff = nb - self.row_nb
                if diff > 0:
                    for i in range(diff // 2):
                        self.add_row()
                elif diff < 0:
                    for i in range((-diff) // 2):
                        self.del_row()
        self.row_nb = self.row_nb
        self.focus_set()

    def add_row(self, event=None, write_log=True, g_out=None, fil_noeud=None):
        """ ajoute 2 lignes """
        if write_log:
            self._log()
            with open(cst.BRACELET_LOG, "a") as log:
                log.write("add_row\n")

        if not g_out:
            g_out = ("1" * len(self.noeuds[0]), "1" * len(self.noeuds[1]))
        if not fil_noeud:
            fil_noeud = ("0" * len(self.noeuds[0]), "0" * len(self.noeuds[1]))
        i = self.row_nb
        self.row_nb += 2
        self.motif += [[], [], [], [], [], [], [], []]
        k = len(self.motif)
        for noeud in self.noeuds[-1]:
            noeud.set_bords(fin=False)
        self.noeuds[-2][0].set_bords(sans_noeud_fin=False)
        self.noeuds[-2][-1].set_bords(sans_noeud_fin=False)
        self.noeuds.append([])
        self.motif2.append([])
        self.motif3.append([])
        nb_noeuds = self.string_nb // 2
        for j in range(nb_noeuds):
            self.noeuds[i].append(Noeud(self.can, 50 + j * 60, 10 + (i + 1) * 30,
                                        color_d=self.color,
                                        color_g=self.color))
            n = self.noeuds[i][-1]
            n.set_g_out(int(g_out[0][j]))
            n.set_fil_noeud(int(fil_noeud[0][j]))
            self._attribue_noeud(i, j)
            self.motif[k - 8].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                   20 + (k - 8) // 2 * 16))
            self.motif[k - 6].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                   20 + (k - 6) // 2 * 16))
            self.motif[k - 4].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                   20 + (k - 4) // 2 * 16))
            self.motif[k - 2].append(self._carreau(self.fin_noeud + 20 + j * 16,
                                                   20 + (k - 2) // 2 * 16))
            self.motif2[i].append([self.color, self.color])
            self.motif3[i].append([self.color, self.color])
        self.noeuds.append([])
        self.motif2.append([])
        self.motif3.append([])
        i += 1
        self.row_numbers.append(self.can.create_text(10, 25 + (i + 1) * 30,
                                                     text="%i" % (i + 1),
                                                     anchor="e",
                                                     font=("Arial", '12')))
        nb_noeuds = self.string_nb // 2 - 1 + self.string_nb % 2
        for j in range(nb_noeuds):
            self.noeuds[i].append(Noeud(self.can, 80 + j * 60, 10 + (i + 1) * 30,
                                        fin=True, color_d=self.color,
                                        color_g=self.color))
            self._attribue_noeud(i, j)
            n = self.noeuds[i][-1]
            n.set_g_out(int(g_out[1][j]))
            n.set_fil_noeud(int(fil_noeud[1][j]))
            self.motif[k - 7].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                   28 + (k - 7) // 2 * 16))
            self.motif[k - 5].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                   28 + (k - 5) // 2 * 16))
            self.motif[k - 3].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                   28 + (k - 3) // 2 * 16))
            self.motif[k - 1].append(self._carreau(self.fin_noeud + 28 + j * 16,
                                                   28 + (k - 1) // 2 * 16))
            self.motif2[i].append([self.color, self.color])
            self.motif3[i].append([self.color, self.color])
        self.noeuds[-2][0].set_bords(bord_g=True, sans_noeud_fin=True)
        if self.string_nb % 2:
            self.noeuds[-1][-1].set_bords(bord_d=True)
        else:
            self.noeuds[-2][-1].set_bords(bord_d=True, sans_noeud_fin=True)
        for j, n in enumerate(self.noeuds[i - 2]):
            self._change_color(i - 2, j, 0, n.get_color(0))
            self._change_color(i - 2, j, 1, n.get_color(1))
        n = self.noeuds[i - 3][0]
        self._change_color(i - 3, 0, n.get_g_out(),
                           n.get_color(n.get_g_out()))
        if self.string_nb % 2 == 0:
            j = self.string_nb // 2 - 1
            n = self.noeuds[i - 3][j]
            gout = n.get_g_out()
            self._change_color(i - 3, j, not gout, n.get_color(not gout))

        bbox = self.can.bbox("all")
        self.can.configure(height=min(bbox[3] - bbox[1] + 20, self.height_max),
                           scrollregion=[bbox[0] - 10,
                                         bbox[1] - 10,
                                         bbox[2] + 10,
                                         bbox[3] + 10])
        self._actualise_motif()
        self.is_saved = False

    def del_row(self, event=None, write_log=True):
        """ efface deux lignes """
        if self.row_nb > 2:
            self.can.delete(self.row_numbers[-1])
            self.row_numbers = self.row_numbers[:-1]
            g_out = [[], []]
            fil_noeud = [[], []]
            for noeud in self.noeuds[-1]:
                g_out[1].append(noeud.get_g_out())
                fil_noeud[1].append(noeud.get_fil_noeud())
                noeud.efface()
            for noeud in self.noeuds[-2]:
                g_out[0].append(noeud.get_g_out())
                fil_noeud[0].append(noeud.get_fil_noeud())
                noeud.efface()
            for ligne in self.motif[-8:]:
                for _carreau in ligne:
                    self.can.delete(_carreau)
            self.noeuds = self.noeuds[:-2]
            self.motif2 = self.motif2[:-2]
            self.motif3 = self.motif3[:-2]
            self.row_nb -= 2
            for noeud in self.noeuds[-1]:
                noeud.set_bords(fin=True)
            self.noeuds[-2][0].set_bords(sans_noeud_fin=True)
            if self.string_nb % 2 == 0:
                self.noeuds[-2][-1].set_bords(sans_noeud_fin=True)
            bbox = self.can.bbox("all")
            self.can.configure(height=min(bbox[3] - bbox[1] + 20,
                                          self.height_max),
                               scrollregion=[bbox[0] - 10,
                                             bbox[1] - 10,
                                             bbox[2] + 10,
                                             bbox[3] + 10])
            self.motif = self.motif[:-8]
            self._actualise_motif()
            self.is_saved = False
            txt_g_out = ""
            txt_fil_noeud = ""
            for i in range(len(g_out[0])):
                txt_g_out += str(g_out[0][i])
                txt_fil_noeud += str(fil_noeud[0][i])
            txt_g_out += " "
            txt_fil_noeud += " "
            for i in range(len(g_out[1])):
                txt_g_out += str(g_out[1][i])
                txt_fil_noeud += str(fil_noeud[1][i])
            if write_log:
                self._log()
                with open(cst.BRACELET_LOG, "a") as log:
                    log.write("del_row %s %s\n" % (txt_g_out, txt_fil_noeud))

    def change_string_nb(self, event=None):
        ch = self.string_nb_entry.get()
        if ch:
            nb = int(ch)
            if nb >= 3:
                diff = nb - self.string_nb
                if diff > 0:
                    for i in range(diff):
                        self.add_string()
                elif diff < 0:
                    for i in range(-diff):
                        self.del_string()
            else:
                self.string_nb = self.string_nb
        else:
            self.string_nb = self.string_nb
        self.focus_set()

    def add_string(self, event=None, write_log=True, color=None, g_out=None, fil_noeud=None):
        """ ajoute un fil au bracelet"""
        if not color:
            color = self.color
        if not g_out:
            g_out = "1" * (self.row_nb // 2)
        if not fil_noeud:
            fil_noeud = "0" * (self.row_nb // 2)
        if write_log:
            self._log()
            with open(cst.BRACELET_LOG, "a") as log:
                log.write("add_string\n")
        self.string_nb += 1
        self.fin_noeud = (self.string_nb - 1) * 30 + 80
        nb = self.string_nb - 1

        # décalage du motif
        for i in range(len(self.motif)):
            for j in range(len(self.motif[i])):
                if i % 2:
                    self._translate_carreau(i, j, self.fin_noeud + 28 + j * 16,
                                            28 + i // 2 * 16)
                else:
                    self._translate_carreau(i, j, self.fin_noeud + 20 + j * 16,
                                            20 + i // 2 * 16)
        nb_noeuds = self.string_nb // 2 - 1
        if self.string_nb % 2:
            for i in range(1, self.row_nb, 2):
                self.noeuds[i - 1][-1].set_bords(bord_d=False)
                self.noeuds[i].append(Noeud(self.can, 80 + nb_noeuds * 60,
                                            10 + (i + 1) * 30, bord_d=True,
                                            color_d=color,
                                            color_g=color))
                n = self.noeuds[i][-1]
                n.set_g_out(int(g_out[i // 2]))
                n.set_fil_noeud(int(fil_noeud[i // 2]))
                self._attribue_noeud(i, nb_noeuds)
                self.motif2[i].append([color, color])
                self.motif3[i].append([color, color])
                self.motif[i].append(self._carreau(self.fin_noeud + 28 + nb_noeuds * 16,
                                                   28 + i // 2 * 16))
                self.motif[i + self.row_nb].append(self._carreau(self.fin_noeud + 28 + nb_noeuds * 16,
                                                                 28 + (i + self.row_nb) // 2 * 16))
                self.motif[i + 2 * self.row_nb].append(self._carreau(self.fin_noeud + 28 + nb_noeuds * 16,
                                                                     28 + (i + self.row_nb * 2) // 2 * 16))
                self.motif[i + 3 * self.row_nb].append(self._carreau(self.fin_noeud + 28 + nb_noeuds * 16,
                                                                     28 + (i + self.row_nb * 3) // 2 * 16))
            self.noeuds[1][-1].set_bords(sans_noeud_deb=True)
            self.noeuds[-1][-1].set_bords(fin=True)

        else:
            for i in range(0, self.row_nb, 2):
                self.noeuds[i + 1][-1].set_bords(bord_d=False)
                self.noeuds[i].append(Noeud(self.can, 50 + nb // 2 * 60,
                                            10 + (i + 1) * 30, bord_d=True,
                                            color_d=self.color,
                                            color_g=self.color))
                n = self.noeuds[i][-1]
                n.set_g_out(int(g_out[i // 2]))
                n.set_fil_noeud(int(fil_noeud[i // 2]))
                self._attribue_noeud(i, nb // 2)
                self.motif2[i].append([color, color])
                self.motif3[i].append([color, color])
                self.motif[i].append(self._carreau(self.fin_noeud + 20 + nb_noeuds * 16,
                                                   20 + i // 2 * 16))
                self.motif[i + self.row_nb].append(self._carreau(self.fin_noeud + 20 + nb_noeuds * 16,
                                                                 20 + (i + self.row_nb) // 2 * 16))
                self.motif[i + 2 * self.row_nb].append(self._carreau(self.fin_noeud + 20 + nb_noeuds * 16,
                                                                     20 + (i + 2 * self.row_nb) // 2 * 16))
                self.motif[i + 3 * self.row_nb].append(self._carreau(self.fin_noeud + 20 + nb_noeuds * 16,
                                                                     20 + (i + 3 * self.row_nb) // 2 * 16))
            self.noeuds[0][-1].set_bords(deb=True)
            self.noeuds[-2][-1].set_bords(sans_noeud_fin=True)

        self.string_numbers.append(self.can.create_text(45 + 30 * nb, 9,
                                                        text="%i" % (nb + 1),
                                                        anchor="s",
                                                        font=("Arial", '12')))
        self.colors.append(self.can.create_rectangle(41 + 30 * nb,
                                                     13, 49 + 30 * nb, 21,
                                                     fill=color,
                                                     activefill=cst.active_color(color)))
        self._attribue_carre(nb)

        for j in range(len(self.noeuds[0])):
            c0 = self.can.itemcget(self.colors[j * 2], 'fill')
            c1 = self.can.itemcget(self.colors[j * 2 + 1], 'fill')
            self._change_color(0, j, 0, c0)
            self._change_color(0, j, 1, c1)
        if self.string_nb % 2:
            c = self.noeuds[1][-1].get_color(1)
            self._change_color(1, nb_noeuds, 1, c)
        bbox = self.can.bbox("all")
        self.can.configure(width=min(self.width_max,
                                     max(bbox[2] - bbox[0] + 20, 230)),
                           scrollregion=[bbox[0] - 10,
                                         bbox[1] - 10,
                                         bbox[2] + 10,
                                         bbox[3] + 10])
        self._actualise_motif()

        self.is_saved = False

    def del_string(self, event=None, write_log=True):
        """ efface un fil """
        if self.string_nb > 3:
            g_out = []
            fil_noeud = []
            coul = self.can.itemcget(self.colors[-1], "fill")
            self.string_nb -= 1
            self.fin_noeud = (self.string_nb - 1) * 30 + 80

            self.can.delete(self.colors[-1])
            self.colors = self.colors[:-1]
            self.can.delete(self.string_numbers[-1])
            self.string_numbers = self.string_numbers[:-1]

            # décalage du motif
            for i in range(len(self.motif)):
                for j in range(len(self.motif[i])):
                    if i % 2:
                        self._translate_carreau(i, j, self.fin_noeud + 28 + j * 16,
                                                28 + i // 2 * 16)
                    else:
                        self._translate_carreau(i, j, self.fin_noeud + 20 + j * 16,
                                                20 + i // 2 * 16)

            nb_noeuds = self.string_nb // 2 - 1
            if self.string_nb % 2 == 0:
                for i in range(1, self.row_nb, 2):
                    self.noeuds[i - 1][-1].set_bords(bord_d=True)
                    n = self.noeuds[i][-1]
                    g_out.append(n.get_g_out())
                    fil_noeud.append(n.get_fil_noeud())
                    n.efface()
                    self.noeuds[i] = self.noeuds[i][:-1]
                    self.motif2[i] = self.motif2[i][:-1]
                    self.motif3[i] = self.motif3[i][:-1]
                    self.can.delete(self.motif[i][-1])
                    self.can.delete(self.motif[i + self.row_nb][-1])
                    self.can.delete(self.motif[i + 2 * self.row_nb][-1])
                    self.can.delete(self.motif[i + 3 * self.row_nb][-1])
                    self.motif[i] = self.motif[i][:-1]
                    self.motif[i + self.row_nb] = self.motif[i + self.row_nb][:-1]
                    self.motif[i + 2 * self.row_nb] = self.motif[i + 2 * self.row_nb][:-1]
                    self.motif[i + 3 * self.row_nb] = self.motif[i + 3 * self.row_nb][:-1]

                self.noeuds[0][-1].set_bords(deb=True)
                self.noeuds[-2][-1].set_bords(sans_noeud_fin=True)

            else:
                for i in range(0, self.row_nb, 2):
                    self.noeuds[i + 1][-1].set_bords(bord_d=True)
                    n = self.noeuds[i][-1]
                    g_out.append(n.get_g_out())
                    fil_noeud.append(n.get_fil_noeud())
                    n.efface()
                    self.noeuds[i] = self.noeuds[i][:-1]
                    self.motif2[i] = self.motif2[i][:-1]
                    self.motif3[i] = self.motif3[i][:-1]
                    self.can.delete(self.motif[i][-1])
                    self.can.delete(self.motif[i + self.row_nb][-1])
                    self.can.delete(self.motif[i + 2 * self.row_nb][-1])
                    self.can.delete(self.motif[i + 3 * self.row_nb][-1])
                    self.motif[i] = self.motif[i][:-1]
                    self.motif[i + self.row_nb] = self.motif[i + self.row_nb][:-1]
                    self.motif[i + 2 * self.row_nb] = self.motif[i + 2 * self.row_nb][:-1]
                    self.motif[i + 3 * self.row_nb] = self.motif[i + 3 * self.row_nb][:-1]

                self.noeuds[1][-1].set_bords(sans_noeud_deb=True)
                self.noeuds[-1][-1].set_bords(fin=True)

            for j, n in enumerate(self.noeuds[0]):
                c0 = n.get_color(0)
                c1 = n.get_color(1)
                self._change_color(0, j, 0, c0)
                self._change_color(0, j, 1, c1)
            if self.string_nb % 2:
                c = self.can.itemcget(self.colors[-1], 'fill')
                self._change_color(1, nb_noeuds, 1, c)
            bbox = self.can.bbox("all")
            self.can.configure(width=min(self.width_max,
                                         max(bbox[2] - bbox[0] + 20, 230)),
                               scrollregion=[bbox[0] - 10,
                                             bbox[1] - 10,
                                             bbox[2] + 10,
                                             bbox[3] + 10])
            self._actualise_motif()
            self.is_saved = False
            txt_g_out = ""
            txt_fil_noeud = ""
            for i in range(len(g_out)):
                txt_g_out += str(g_out[i])
                txt_fil_noeud += str(fil_noeud[i])
            if write_log:
                self._log()
                with open(cst.BRACELET_LOG, "a") as log:
                    log.write("del_string %s %s %s\n" % (coul, txt_g_out,
                                                         txt_fil_noeud))

    def symmetrize(self, sens, write_log=True):
        """ symétrise le motif selon l'axe sens """
        if sens == "horizontal":
            if self.string_nb % 2 == 0:
                string_nb = self.string_nb * 2
                fils = []
                for noeud in self.noeuds[0]:
                    fils.append([noeud.get_color(0), noeud.get_color(1)])
                for noeud in reversed(fils):
                    fils.append([noeud[1], noeud[0]])
                g_out = []
                fil_noeud = []
                for ligne in self.noeuds:
                    g_out.append([])
                    fil_noeud.append([])
                    for n in ligne:
                        g_out[-1].append(n.get_g_out())
                        fil_noeud[-1].append(n.get_fil_noeud())
                l = [1, 0]
                for i in range(self.row_nb):
                    if i % 2:
                        g_out[i] = g_out[i] + [1] + list(reversed(g_out[i]))
                        fil_noeud[i] = fil_noeud[i] + [0] + [l[k] for k in reversed(fil_noeud[i])]
                    else:
                        g_out[i] = g_out[i] + list(reversed(g_out[i]))
                        fil_noeud[i] = fil_noeud[i] + [l[k] for k in reversed(fil_noeud[i])]
                self.string_nb = string_nb
                self.init_canvas()
                self._importe(fils, g_out, fil_noeud)

            else:
                string_nb = self.string_nb * 2
                fils = []
                for noeud in self.noeuds[0]:
                    fils.append([noeud.get_color(0), noeud.get_color(1)])
                coul = self.noeuds[1][-1].get_color(1)
                fils.append([coul, coul])
                for noeud in reversed(fils[:-1]):
                    fils.append([noeud[1], noeud[0]])
                g_out = []
                fil_noeud = []
                for ligne in self.noeuds:
                    g_out.append([])
                    fil_noeud.append([])
                    for n in ligne:
                        g_out[-1].append(n.get_g_out())
                        fil_noeud[-1].append(n.get_fil_noeud())
                l = [1, 0]
                for i in range(self.row_nb):
                    if i % 2 == 0:
                        g_out[i] = g_out[i] + [1] + list(reversed(g_out[i]))
                        fil_noeud[i] = fil_noeud[i] + [0] + [l[k] for k in reversed(fil_noeud[i])]
                    else:
                        g_out[i] = g_out[i] + list(reversed(g_out[i]))
                        fil_noeud[i] = fil_noeud[i] + [l[k] for k in reversed(fil_noeud[i])]
                self.string_nb = string_nb
                self.init_canvas()
                self._importe(fils, g_out, fil_noeud)
            if write_log:
                self._log()
                with open(cst.BRACELET_LOG, "a") as log:
                    log.write("symmetrize %s\n" % (sens))
        if sens == "vertical":
            fils = []
            for noeud in self.noeuds[0]:
                fils.append([noeud.get_color(0), noeud.get_color(1)])
            if self.string_nb % 2:
                fils.append([self.noeuds[1][-1].get_color(1)])
            g_out = []
            fil_noeud = []
            for ligne in self.noeuds:
                g_out.append([])
                fil_noeud.append([])
                for n in ligne:
                    g_out[-1].append(n.get_g_out())
                    fil_noeud[-1].append(n.get_fil_noeud())
            txtlog = ""
            for n in g_out[-1]:
                txtlog += str(n)
            g_out[-1] = [0] * len(g_out[-1])
            l = [1, 0]
            for lg, lf in zip(reversed(g_out[:-1]), reversed(fil_noeud[:-1])):
                g_out.append(lg)
                fil_noeud.append([])
                for g, f in zip(lg, lf):
                    if g:
                        fil_noeud[-1].append(l[f])
                    else:
                        fil_noeud[-1].append(f)
            g_out.append(g_out[self.row_nb - 1])
            fil_noeud.append([l[k] for k in fil_noeud[self.row_nb - 1]])
            self.row_nb = self.row_nb * 2
            self.init_canvas()
            self._importe(fils, g_out, fil_noeud)
            if write_log:
                self._log()
                with open(cst.BRACELET_LOG, "a") as log:
                    log.write("symmetrize %s %s\n" % (sens, txtlog))

        self.is_saved = False

    def add_recent_file(self, file):
        """ ajoute fichier aux fichiers récents,
            supprime le plus ancien s'il y en a plus de 10,
            actualise le menu des fichiers récents """
        if not cst.RECENT_FILES:
            self.menu_file.entryconfigure(3, state="normal")
        if file in cst.RECENT_FILES:
            i = cst.RECENT_FILES.index(file)
            self.menu_recent_files.delete(i)
            cst.RECENT_FILES.remove(file)

        cst.RECENT_FILES.insert(0, file)
        self.menu_recent_files.insert_command(0, label=file,
                                              command=lambda: self.open(fichier=file))
        if len(cst.RECENT_FILES) > 10:
            self.menu_recent_files.delete(10)
            del(cst.RECENT_FILES[-1])

    def del_recent_file(self, file):
        """ supprime file aux fichiers récents (de l'éditeur de motifs et du logiciel),
            actualise le menu des fichiers récents """
        if file in cst.RECENT_FILES:
            i = cst.RECENT_FILES.index(file)
            self.menu_recent_files.delete(i)
            cst.RECENT_FILES.remove(file)

        if not cst.RECENT_FILES:
            self.menu_file.entryconfigure(3, state="disabled")

        if file in cst.RECENT_BICOLOR:
            cst.RECENT_BICOLOR.remove(file)

    def _importe(self, fils, g_out, fil_noeud):
        """ importe les informations sur le motif et actualise le bracelet """
        for i in range(self.row_nb):
            for n, g, f in zip(self.noeuds[i], g_out[i], fil_noeud[i]):
                n.set_g_out(g)
                n.set_fil_noeud(f)
        for j, n in enumerate(self.noeuds[0]):
            c0 = fils[j][0]
            c1 = fils[j][1]
            self.can.itemconfigure(self.colors[2 * j], fill=c0,
                                   activefill=cst.active_color(c0))
            self.can.itemconfigure(self.colors[2 * j + 1], fill=c1,
                                   activefill=cst.active_color(c1))
            self._change_color(0, j, 0, c0)
            self._change_color(0, j, 1, c1)
        if self.string_nb % 2:
            c = fils[-1][0]
            self._change_color(1, j, 1, c)
            self.can.itemconfigure(self.colors[self.string_nb - 1], fill=c,
                                   activefill=cst.active_color(c))
        self._actualise_motif()
        self.is_saved = True

    def _log(self):
        """ annule la possibilté de faire redo une fois qu'on a
            remodifié le bracelet """
        self.log_nb_ligne += 1
        self.log_ligne += 1
        self.menu_edit.entryconfigure(0, state="normal")
        if self.log_ligne != self.log_nb_ligne - 1:
            self.menu_edit.entryconfigure(1, state="disabled")
            with open(cst.BRACELET_LOG, "r") as log:
                logfile = log.readlines()
            with open(cst.BRACELET_LOG, "w") as log:
                # supprime les actions annulées précédemment
                for ligne in logfile[:self.log_ligne]:
                    log.write(ligne)
        self.log_nb_ligne = self.log_ligne + 1

    def about(self):
        """ ouvre la fenêtre 'à propos de Bracelet Generator' """
        About(self)

    def new(self, event=None):
        """ ouvre la fenêtre de paramétrage d'un new bracelet,
            le bracelet en cours sera effacé """
        rep = False
        if not self.is_saved:
            rep = askyesnocancel('Question',
                                 _("The pattern has not been saved. Do you want to save it before replacing it by a new one?"),
                                 icon="warning")
            if rep:
                self.save()
        if rep is not None:
            self.init_canvas()
            self.path_save = ""
            self._logreinit()

    def manage_colors(self, event=None):
        """ ouvre une fenêtre permettant de remplacer les colors actuelles par de nouvelles """
        couls = [self.can.itemcget(j, "fill") for j in self.colors]
        # enlève les répétitions de colors
        c_colors = set(couls)
        # ouvre l'interface de gestion
        manager = Couleurs(self, self.color, c_colors)
        manager.lift(self)
        self.wait_window(manager)
        res = manager.get_result()
        if res:
            # des colors ont été changées
            color, n_colors = res
            dic_coul = {c: n for c, n in zip(c_colors, n_colors)}
            for j, c in enumerate(couls):
                self._select_color(j, write_log=False, color=dic_coul[c])
            # écriture dans le log
            self._log()
            with open(cst.BRACELET_LOG, "a") as log:
                c = ", ".join(c_colors)
                n = ", ".join(n_colors)
                # action ancien_défaut nv_défaut c_colors n_colors
                log.write("color_manager %s %s %s %s\n" % (self.color, color, c, n))
            self.color = color
            self.is_saved = False

    def open(self, event=None, fichier=""):
        """ ouvre un bracelet enregistré dans un fichier .bracelet """
        rep = False
        if not self.is_saved:
            rep = askyesnocancel('Question',
                                 _("The pattern has not been saved. Do you want to save it before replacing it by another one?"),
                                 icon="warning")
            if rep:
                self.save()
        if rep is not None:
            if not fichier:
                fichier = cst.askopenfilename(defaultextension='.bracelet',
                                              filetypes=[('BRACELET', '*.bracelet'),
                                                         ('BICOLOR', '*.bicolor')],
                                              initialdir=cst.CONFIG.get("General", "last_path"))
            if fichier:
                if os.path.exists(fichier):
                    cst.CONFIG.set("General", "last_path", os.path.dirname(fichier))
                    if fichier.split(".")[-1] == "bicolor":
                        self.init_canvas()
                        self._logreinit()
                        self.bicolore(fichier=fichier)
                        self.path_save = ""  # saved pattern path
                        self.add_recent_file(file=fichier)
                    elif fichier.split(".")[-1] == "bracelet":
                        with open(fichier, "rb") as fich:
                            dp = Unpickler(fich)
                            self.row_nb = dp.load()
                            self.string_nb = dp.load()
                            self.color = dp.load()
                            fils = dp.load()
                            g_out = dp.load()
                            fil_noeud = dp.load()
                        self.init_canvas()
                        self._importe(fils, g_out, fil_noeud)
                        self.path_save = fichier
                        self._logreinit()
                        self.add_recent_file(file=fichier)

                    else:  # il y a eu une erreur
                        showerror(_("Error"),
                                  _("The file %(name)s is not a valid pattern file.") % ({"name": os.path.split(fichier)[-1]}))
                else:
                    showerror(_("Error"),
                              _("The file %(name)s does not exists.") % ({"name": fichier}))
                    self.del_recent_file(fichier)

    def saveas(self, event=None):
        """ demande le chemin d'enristrement puis sauve le bracelet
            (fct saver sous) """
        if self.path_save:
            initialdir, initialfile = os.path.split(self.path_save)
        else:
            initialdir = cst.CONFIG.get("General", "last_path")
            initialfile = ""
        fichier = cst.asksaveasfilename(defaultextension='.bracelet',
                                        filetypes=[('BRACELET', '*.bracelet')],
                                        initialdir=initialdir,
                                        initialfile=initialfile)
        if fichier:
            ext = os.path.splitext(fichier)[-1]
            self.add_recent_file(file=fichier)
            cst.CONFIG.set("General", "last_path", os.path.dirname(fichier))
            if ext == ".bracelet":
                self.save(fichier=fichier)
                self.path_save = fichier
            else:
                showerror(_("Error"),
                          _("%(extension)s is not a valid extension for a pattern file.") % ({"extension": ext}))

    def save(self, event=None, fichier=None):
        """ save the pattern """
        if not self.is_saved:
            if fichier is None and not self.path_save:
                self.saveas()
            else:
                if fichier is None:
                    fichier = self.path_save
                fils = []
                for noeud in self.noeuds[0]:
                    fils.append([noeud.get_color(0), noeud.get_color(1)])
                if self.string_nb % 2:
                    fils.append([self.noeuds[1][-1].get_color(1)])
                g_out = []
                fil_noeud = []
                for ligne in self.noeuds:
                    g_out.append([])
                    fil_noeud.append([])
                    for n in ligne:
                        g_out[-1].append(n.get_g_out())
                        fil_noeud[-1].append(n.get_fil_noeud())
                with open(fichier, 'wb') as fichier:
                    p = Pickler(fichier)
                    p.dump(self.row_nb)
                    p.dump(self.string_nb)
                    p.dump(self.color)
                    p.dump(fils)
                    p.dump(g_out)
                    p.dump(fil_noeud)
                self.is_saved = True

    def export(self, event=None):
        """ exporte le patron en .ps, .eps, .png ou .jpg """
        if self.path_save:
            initialdir, initialfile = os.path.split(self.path_save)
            initialfile = os.path.splitext(initialfile)[0] + ".png"
        else:
            initialdir = cst.CONFIG.get("General", "last_path")
            initialfile = ""

        fichier = cst.asksaveasfilename(title=_("Export"),
                                        defaultextension='.png',
                                        filetypes=[('PNG', '*.png'),
                                                   ('JPEG', '*.jpg'),
                                                   ('EPS', '*.eps'),
                                                   ('PS', '*.ps')],
                                        initialdir=initialdir,
                                        initialfile=initialfile)
        if fichier:
            ext = os.path.splitext(fichier)[-1]
            ext = ext[1:]
            cst.CONFIG.set("General", "last_path", os.path.dirname(fichier))
        else:
            ext = ""

        box = self.can.bbox("all")
        if ext in ["ps", "eps"]:
            self.can.postscript(file=fichier, colormode='color',
                                height=box[3] + 20, width=box[2] + 20,
                                x=box[0] - 10, y=box[1] - 10)
        elif ext in ["png", "jpg"]:
            self.can.postscript(file=cst.TMP_PS, colormode='color',
                                height=box[3] + 20, width=box[2] + 20,
                                x=box[0] - 10, y=box[1] - 10)

            im = Image.open(cst.TMP_PS)
            im.load(scale=6)
            im.save(fichier)
            im.close()
            os.remove(cst.TMP_PS)
        elif fichier:
            showerror(_("Error"),
                      _("The pattern cannot be exported in .%(extension)s") % ({"extension": ext}))

    def export_txt(self, event=None):
        """ export the pattern to text format:
                * forward knot = 0
                * backward knot = 1
                * backward forward = 2
                * forward backward = 3 """
        if self.path_save:
            initialdir, initialfile = os.path.split(self.path_save)
            initialfile = os.path.splitext(initialfile)[0] + ".txt"
        else:
            initialdir = cst.CONFIG.get("General", "last_path")
            initialfile = ""

        fichier = cst.asksaveasfilename(title=_("Export"),
                                        defaultextension='.txt',
                                        filetypes=[('TXT', '*.txt')],
                                        initialdir=initialdir,
                                        initialfile=initialfile)
        if fichier:
            cst.CONFIG.set("General", "last_path", os.path.dirname(fichier))
            rows = []
            for row in self.noeuds:
                knots = ["%i" % knot.get_code() for knot in row]
                rows.append("".join(knots))

            with open(fichier, "w") as file:
                file.write(_("0: forward knot, 1: backward knot, 2: backward forward, 3: forward backward\n\n"))
                file.write(_("strings: {string_nb}, rows: {row_nb}\n\n").format(string_nb=self.string_nb, row_nb=self.row_nb))
                file.write("\n".join(rows))

    def bicolore(self, event=None, fichier=""):
        """ ouvre l'éditeur de motifs bicolores """
        rep = False
        if not fichier and not self.is_saved:
            rep = askyesnocancel('Question',
                                 _("The pattern has not been saved. Do you want to save it before replacing it by another one?"),
                                 icon="warning")
            if rep:
                self.save()
        if rep is not None:
            bg = self.color
            if bg != "#141414":
                fg = "#141414"
            else:
                fg = "#ffffff"
            self.bicolore_on = True
            self.bic = Bicolore(self, self.row_nb, self.string_nb,
                                bg, fg, fichier)
            self.bic.lift(self)
            self.wait_window(self.bic)
            bi = self.bic.get_result()
            self.bicolore_on = False
            if bi:
                self.row_nb, self.string_nb, colors, motif = bi
                self.color = colors[0]
                fils = [colors for i in range(self.string_nb // 2)]
                if self.string_nb % 2:
                    fils.append(colors[0:1])
                g_out = []
                fil_noeud = []
                for i in range(self.row_nb):
                    g_out.append([])
                    fil_noeud.append([])
                    for n in motif[i]:
                        if i % 2:
                            fil_noeud[i].append(int(not n))
                        else:
                            fil_noeud[i].append(n)
                        g_out[i].append(0)
                self.init_canvas()
                self._importe(fils, g_out, fil_noeud)
                self.is_saved = False
                self._logreinit()

    def exit(self, event=None):
        """ demande confirmation (ou propose d'saver) et quitte """
        cst.CONFIG.set("Bracelet", "string_nb", "%i" % self.string_nb)
        cst.CONFIG.set("Bracelet", "row_nb", "%i" % self.row_nb)
        cst.CONFIG.set("Bracelet", "default_color", self.color)
        if not self.bicolore_on:
            if not self.is_saved:
                rep = askyesnocancel('Question',
                                     _("The pattern has not been saved. Do you want to save it before closing?"))
                if rep is not None:
                    if rep:
                        self.save()
                    self.destroy()
            else:
                self.destroy()
        else:
            try:
                quitter = self.bic.exit()
            except AttributeError:
                # le générateur de motifs bicolores a planté
                quitter = True
            if quitter:
                self.bicolore_on = False
                self.exit()

    def undo(self, event=None):
        """ annule la dernière action """
        if self.log_ligne > 1:
            with open(cst.BRACELET_LOG, "r") as log:
                logfile = log.readlines()
            self.menu_edit.entryconfigure(1, state="normal")
            txt = logfile[self.log_ligne].split()
            self.log_ligne -= 1
            if self.log_ligne == 1:
                self.menu_edit.entryconfigure(0, state="disabled")
            if txt[0] == "add_string":
                self.del_string(write_log=False)
            elif txt[0] == "add_row":
                self.del_row(write_log=False)
            elif txt[0] == "change_color":
                self._select_color(int(txt[1]), write_log=False,
                                   color=txt[2])
            elif txt[0] == "color_manager":
                # color par défaut
                self.color = txt[1]
                # color des fils
                c_colors = txt[3].split(", ")
                n_colors = txt[4].split(", ")
                dic_coul = {n: c for c, n in zip(c_colors, n_colors)}
                couls = [self.can.itemcget(j, "fill") for j in self.colors]
                for j, c in enumerate(couls):
                    self._select_color(j, write_log=False, color=dic_coul[c])
            elif txt[0] == "clic_noeud":
                self._clic_noeud_inv(int(txt[1]), int(txt[2]), False)
            elif txt[0] == "clic_noeud_inv":
                self._clic_noeud(int(txt[1]), int(txt[2]), False)
            elif txt[0] == "del_string":
                self.add_string(write_log=False, color=txt[1], g_out=txt[2],
                                fil_noeud=txt[3])
            elif txt[0] == "del_row":
                self.add_row(write_log=False, g_out=(txt[1], txt[2]),
                             fil_noeud=(txt[3], txt[4]))
            elif txt[0] == "symmetrize":
                if txt[1] == "horizontal":
                    string_nb = self.string_nb // 2
                    for i in range(string_nb):
                        self.del_string(write_log=False)
                elif txt[1] == "vertical":
                    nb = self.row_nb // 4
                    for i in range(nb):
                        self.del_row(write_log=False)
                    for n, g in zip(self.noeuds[-1], txt[2]):
                        n.set_g_out(int(g))
                    self._actualise_motif()

    def redo(self, event=None):
        """ rétablit la dernière action annulée """
        if self.log_ligne < self.log_nb_ligne - 1:
            self.menu_edit.entryconfigure(0, state="normal")
            with open(cst.BRACELET_LOG, "r") as log:
                logfile = log.readlines()
            self.log_ligne += 1
            if self.log_ligne == self.log_nb_ligne - 1:
                self.menu_edit.entryconfigure(1, state="disabled")
            txt = logfile[self.log_ligne].split()
            if txt[0] == "add_string":
                self.add_string(write_log=False)
            elif txt[0] == "add_row":
                self.add_row(write_log=False)
            elif txt[0] == "change_color":
                self._select_color(int(txt[1]), write_log=False,
                                   color=txt[3])
            elif txt[0] == "color_manager":
                # color par défaut
                self.color = txt[2]
                # color des fils
                c_colors = txt[3].split(", ")
                n_colors = txt[4].split(", ")
                dic_coul = {c: n for c, n in zip(c_colors, n_colors)}
                couls = [self.can.itemcget(j, "fill") for j in self.colors]
                for j, c in enumerate(couls):
                    self._select_color(j, write_log=False, color=dic_coul[c])
            elif txt[0] == "clic_noeud":
                self._clic_noeud(int(txt[1]), int(txt[2]), False)
            elif txt[0] == "clic_noeud_inv":
                self._clic_noeud_inv(int(txt[1]), int(txt[2]), False)
            elif txt[0] == "del_string":
                self.del_string(write_log=False)
            elif txt[0] == "del_row":
                self.del_row(write_log=False)
            elif txt[0] == "symmetrize":
                self.symmetrize(txt[1], write_log=False)

    def _logreinit(self):
        """ réinitialise le fichier log
            (ie efface l'historique des actions) """
        with open(cst.BRACELET_LOG, "w") as log:
            log.write("#Bracelet Generator logfile\n\n")
        self.log_ligne = 1  # ligne actuelle dans le fichier log
        self.log_nb_ligne = 2  # nombre de lignes du fichier log
        self.menu_edit.entryconfigure(0, state="disabled")
        self.menu_edit.entryconfigure(1, state="disabled")

    def _translate(self):
        """ changement de la langue de l'interface """
        showinfo(_("Information"),
                 _("The language setting will take effect after restarting the application"))
        cst.CONFIG.set("General", "language", self.langue.get())
