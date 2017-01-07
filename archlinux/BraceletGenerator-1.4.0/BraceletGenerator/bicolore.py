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

Two-colored pattern generator
"""

from pickle import Pickler, Unpickler
from tkinter import Toplevel, Menu, Canvas, PhotoImage
from tkinter.ttk import Button, Entry, Label, Style, Frame
from tkinter.messagebox import showerror
from tkinter.messagebox import askyesno, askyesnocancel
from BraceletGenerator.constantes import *
from BraceletGenerator.about import About
from BraceletGenerator.scrollbar import AutoScrollbar as Scrollbar


BICOLOR_LOG = os.path.join(LOCAL_PATH, "Bicolor%i.log")
i = 0
while os.path.exists(BICOLOR_LOG % (i)):
    i += 1
BICOLOR_LOG %= i

class Bicolore(Toplevel):
    """ classe de l'application éditeur de motif bicolore """
    def __init__(self, master, row_nb=10, string_nb=8,
                 bg='#ffffff', fg="#ff0000", fichier="", **options):
        """ créer le Toplevel permettant d'éditer des motifs bicolores
            pour ensuite en générer le patron """
        self.colors = [bg, fg]

        # création et paramétrage de la fenêtre
        Toplevel.__init__(self, master, **options)
        g, x, y = self.master.geometry().split("+")
        self.geometry("+%s+%s" % (x,y))

        self.title(_("Motif Editor"))
        self.transient(master)
        self.grab_set()
        self.configure(bg=BG_COLOR)
        set_icon(self)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.height_max = self.winfo_screenheight() - 180
        self.width_max = self.winfo_screenwidth() - 50
        self.minsize(width=410, height=285)
        self.maxsize(width=self.winfo_screenwidth(),
                     height=self.winfo_screenheight())
        self.protocol("WM_DELETE_WINDOW", self.exit)
        # fonction de validation des entrées
        self._okfct = self.register(valide_entree_nb)

        # fichier log
        with open(BICOLOR_LOG, "w") as log:
            log.write("#Bracelet Generator Bicolor logfile\n\n")
        self.log_ligne = 1  # ligne actuelle dans le fichier log
        self.log_nb_ligne = 2  # nombre de lignes du fichier log

        # style
        style = Style(self)
        style.theme_use(STYLE)
        style.configure('TButton', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR)
        style.configure('TFrame', background=BG_COLOR)

        # menu
        self.m_plus = open_image(file=IM_PLUS_M, master=self)
        self.m_moins = open_image(file=IM_MOINS_M, master=self)
        self.m_exit = open_image(file=IM_EXIT_M, master=self)
        self.m_open = open_image(file=IM_OUVRIR_M, master=self)
        self.m_saveas = open_image(file=IM_SAVEAS_M, master=self)
        self.m_save = open_image(file=IM_SAUVER_M, master=self)
        self.m_export = open_image(file=IM_EXPORT_M, master=self)
        self.m_undo = open_image(file=IM_UNDO, master=self)
        self.m_redo = open_image(file=IM_REDO, master=self)
        self.m_clear = open_image(file=IM_EFFACE_M, master=self)
        self.m_help = open_image(file=IM_AIDE, master=self)
        self.m_about = open_image(file=IM_ABOUT, master=self)
        self.m_rotate_cw = open_image(file=IM_ROTATION_DTE_M, master=self)
        self.m_rotate_ccw = open_image(file=IM_ROTATION_GCHE_M, master=self)
        self.m_move = open_image(file=IM_MOVE_M, master=self)
        self.m_sym_vertical = open_image(file=IM_SYM_VERT_M, master=self)
        self.m_sym_horizontal = open_image(file=IM_SYM_HORIZ_M, master=self)
        self.m_move_e = open_image(master=self,file=IM_MOVE_E_M)
        self.m_move_s = open_image(master=self,file=IM_MOVE_S_M)
        self.m_move_w = open_image(master=self,file=IM_MOVE_W_M)
        self.m_move_n = open_image(master=self,file=IM_MOVE_N_M)
        self.m_move_se = open_image(master=self,file=IM_MOVE_SE_M)
        self.m_move_sw = open_image(master=self,file=IM_MOVE_SW_M)
        self.m_move_nw = open_image(master=self,file=IM_MOVE_NW_M)
        self.m_move_ne = open_image(master=self,file=IM_MOVE_NE_M)
        self.m_bg = PhotoImage(width=12, height=12, master=self)
        fill(self.m_bg, self.colors[0])
        self.m_fg = PhotoImage(width=12, height=12, master=self)
        fill(self.m_fg, self.colors[1])

        menu = Menu(self, tearoff=0, borderwidth=0, bg=BG_COLOR)
        # Fichier
        self.menu_file = Menu(menu, tearoff=0, bg=BG_COLOR)
        self.menu_recent_files = Menu(self.menu_file, tearoff=0, bg=BG_COLOR)
        self.menu_file.add_command(label=_("Open"), image=self.m_open,
                                   compound="left", command=self.open,
                                   accelerator='Ctrl+O')
        self.menu_file.add_cascade(label=_("Recent Files"),
                                   image=self.m_open,
                                   compound="left",
                                   menu=self.menu_recent_files)
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Save"), image=self.m_save,
                                   compound="left",
                                   command=self.save,
                                   accelerator='Ctrl+S')
        self.menu_file.add_command(label=_("Save As"), image=self.m_saveas,
                                   compound="left",
                                   command=self.saveas,
                                   accelerator=_("Shift+Ctrl+S"))
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Generate Pattern"),
                                   image=self.m_export, compound="left",
                                   command=self.generate,
                                   accelerator="Ctrl+G")
        self.menu_file.add_separator()
        self.menu_file.add_command(label=_("Quit Editor"),
                                   image=self.m_exit, compound="left",
                                   command=self.exit,
                                   accelerator="Ctrl+Q")

        # Édition
        self.menu_edit = Menu(menu, tearoff=0, bg=BG_COLOR)
        self.menu_edit.add_command(label=_("Undo"), image=self.m_undo,
                                   compound="left", command=self.undo,
                                   accelerator="Ctrl+Z")
        self.menu_edit.add_command(label=_("Redo"), image=self.m_redo,
                                   compound="left", command=self.redo,
                                   accelerator="Ctrl+Y")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Clear"), image=self.m_clear,
                                   compound="left", command=self.clear,
                                   accelerator="Ctrl+X")
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label=_("Background Color"), image=self.m_bg,
                                   compound="left", command=self.set_bg,
                                   accelerator="Ctrl+B")
        self.menu_edit.add_command(label=_("Foreground Color"), image=self.m_fg,
                                   compound="left", command=self.set_fg,
                                   accelerator="Ctrl+F")
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

        # Transformations
        self.menu_transform = Menu(menu, tearoff=0, bg=BG_COLOR)
        menu_move = Menu(self.menu_transform, tearoff=0, bg=BG_COLOR)
        menu_move.add_command(label=_("North"),
                              image=self.m_move_n,
                              compound="left",
                              command=lambda: self.shift("n"),
                              accelerator="↑, Ctrl+8")
        menu_move.add_command(label=_("North-East"),
                              image=self.m_move_ne,
                              compound="left",
                              command=lambda: self.shift("ne"),
                              accelerator="Ctrl+9")
        menu_move.add_command(label=_("East"),
                              image=self.m_move_e,
                              compound="left",
                              command=lambda: self.shift("e"),
                              accelerator="→, Ctrl+6")
        menu_move.add_command(label=_("South-East"),
                              image=self.m_move_se,
                              compound="left",
                              command=lambda: self.shift("se"),
                              accelerator="Ctrl+3")
        menu_move.add_command(label=_("South"),
                              image=self.m_move_s,
                              compound="left",
                              command=lambda: self.shift("s"),
                              accelerator="↓, Ctrl+2")
        menu_move.add_command(label=_("South-West"),
                              image=self.m_move_sw,
                              compound="left",
                              command=lambda: self.shift("sw"),
                              accelerator="Ctrl+1")
        menu_move.add_command(label=_("West"),
                              image=self.m_move_w,
                              compound="left",
                              command=lambda: self.shift("w"),
                              accelerator="←, Ctrl+4")
        menu_move.add_command(label=_("North-West"),
                              image=self.m_move_nw,
                              compound="left",
                              command=lambda: self.shift("nw"),
                              accelerator="Ctrl+7")

        self.menu_transform.add_command(label=_("Shift Motif"),
                                        image=self.m_move,
                                        compound="left",
                                        command=self.shift_motif,
                                        accelerator="Ctrl+M")
        self.menu_transform.add_cascade(label=_("Shift ..."),
                                        compound="left",
                                        menu=menu_move)
        self.menu_transform.add_separator()
        self.menu_transform.add_command(label=_("Rotate Counter-Clockwise"),
                                        image=self.m_rotate_ccw,
                                        compound="left",
                                        command=lambda: self.rotate("ccw"),
                                        accelerator="Ctrl+L")
        self.menu_transform.add_command(label=_("Rotate Clockwise"),
                                        image=self.m_rotate_cw,
                                        compound="left",
                                        command=lambda: self.rotate("cw"),
                                        accelerator="Ctrl+R")
        self.menu_transform.add_separator()
        self.menu_transform.add_command(label=_("Vertical Symmetry"),
                                        command=lambda: self.symmetrize("vertical"),
                                        image=self.m_sym_vertical,
                                        compound="left", accelerator="Ctrl+V")
        self.menu_transform.add_command(label=_("Horizontal Symmetry"),
                                        command=lambda: self.symmetrize("horizontal"),
                                        image=self.m_sym_horizontal,
                                        compound="left", accelerator="Ctrl+H")

        self.menu_help = Menu(menu, tearoff=0, bg=BG_COLOR)
        self.menu_help.add_command(label=_("Help"), image=self.m_help,
                                   command=help, compound="left",
                                   accelerator="F1")
        self.menu_help.add_command(label=_("Online Help"),
                                   image=self.m_help, command=help_web,
                                   compound="left",
                                   accelerator="Ctrl+F1")
        self.menu_help.add_command(label=_("About"), image=self.m_about,
                                   command=self.about, compound="left")

        menu.add_cascade(label=_("File"), menu=self.menu_file)
        menu.add_cascade(label=_("Edit"), menu=self.menu_edit)
        menu.add_cascade(label=_("Transform"), menu=self.menu_transform)
        menu.add_cascade(label=_("Help"), menu=self.menu_help)

        self.menu_edit.entryconfigure(0, state="disabled")
        self.menu_edit.entryconfigure(1, state="disabled")
        self.menu_file.entryconfigure(3, state="disabled")

        if RECENT_BICOLOR:
            for file in RECENT_BICOLOR:
                self.menu_recent_files.add_command(label=file,
                                                   command=lambda fichier=file: self.open(fichier=fichier))
        else:
            self.menu_file.entryconfigure(1, state="disabled")

        self.configure(menu=menu)

        # toolbar
        toolbar = Frame(self, height=24)
        toolbar.grid(row=0, column=0, sticky="ew")

        self.icon_genere = open_image(file=IM_EXPORT, master=self)
        self.icon_efface = open_image(file=IM_EFFACE, master=self)
        self.icon_open = open_image(file=IM_OUVRIR, master=self)
        self.icon_sauve = open_image(file=IM_SAUVER, master=self)
        self.icon_exit = open_image(file=IM_EXIT, master=self)
        self.icon_move = open_image(file=IM_MOVE, master=self)
        self.icon_rotate_ccw = open_image(file=IM_ROTATION_GCHE, master=self)
        self.icon_rotate_cw = open_image(file=IM_ROTATION_DTE, master=self)
        self.icon_sym_vertical = open_image(file=IM_SYM_VERT, master=self)
        self.icon_sym_horizontal = open_image(file=IM_SYM_HORIZ, master=self)

        Button(toolbar, image=self.icon_open,
               command=self.open,
               style='flat.TButton').grid(column=0, row=0)
        self.save_button = Button(toolbar, image=self.icon_sauve,
                                   command=self.save,
                                   style='flat.TButton')
        self.save_button.grid(column=1, row=0)
        Button(toolbar, image=self.icon_genere, command=self.generate,
               style='flat.TButton').grid(column=2, row=0)
        Button(toolbar, image=self.icon_efface, command=self.clear,
               style='flat.TButton').grid(column=3, row=0)
        Button(toolbar, image=self.icon_move,
               command=self.shift_motif,
               style='flat.TButton').grid(column=4, row=0)
        Button(toolbar, image=self.icon_rotate_ccw,
               command=lambda: self.rotate("ccw"),
               style='flat.TButton').grid(column=5, row=0)
        Button(toolbar, image=self.icon_rotate_cw,
               command=lambda: self.rotate("cw"),
               style='flat.TButton').grid(column=6, row=0)
        Button(toolbar, image=self.icon_sym_vertical,
               command=lambda: self.symmetrize("vertical"),
               style='flat.TButton').grid(column=7, row=0)
        Button(toolbar, image=self.icon_sym_horizontal,
               command=lambda: self.symmetrize("horizontal"),
               style='flat.TButton').grid(column=8, row=0)
        Button(toolbar,image = self.icon_exit,command = self.exit,
               style = 'flat.TButton' ).grid(column = 9,row = 0)

        # motif frame
        motif_frame = Frame(self, relief="sunken", borderwidth=1)
        motif_frame.grid(row=1, column=0, sticky="wsen")
        motif_frame.rowconfigure(1, weight=1)
        motif_frame.columnconfigure(0, weight=1)

        # toolbar2
        toolbar2 = Frame(motif_frame, height=24)
        toolbar2.grid(row=0, column=0, sticky="we")

        self.icon_plus = open_image(file=IM_PLUS, master=self)
        self.icon_moins = open_image(file=IM_MOINS, master=self)
        self.icon_bg = PhotoImage(width=16, height=16, master=self)
        fill(self.icon_bg, self.colors[0])
        self.icon_fg = PhotoImage(width=16, height=16, master=self)
        fill(self.icon_fg, self.colors[1])

        self.b_bg = Button(toolbar2, image=self.icon_bg,
                           command=self.set_bg)
        self.b_bg.grid(row=0, column=0, pady=4, padx=2)
        self.b_fg = Button(toolbar2, image=self.icon_fg,
                           command=self.set_fg)
        self.b_fg.grid(row=0, column=1, pady=4, padx=2)

        Label(toolbar2, text=_("Rows: ")).grid(row=0, column=2,
                                               sticky="ewsn", padx=(5,0))
        self.row_nb_entry = Entry(toolbar2, width=3,
                                   validatecommand=(self._okfct, '%d', '%S'),
                                   validate='key', justify="center")
        self.row_nb_entry.grid(row=0, column=3, sticky="w", padx=(0,5))
        Button(toolbar2, image=self.icon_plus,
               command=self.add_row).grid(row=0, column=4, padx=2,
                                                  pady=4)
        Button(toolbar2, image=self.icon_moins,
               command=self.del_row).grid(row=0, column=5, pady=4, padx=2)

        Label(toolbar2, text=_("Strings: ")).grid(row=0, column=6,
                                                  sticky="ewsn", padx=5)
        self.string_nb_entry = Entry(toolbar2, width=3,
                                     validatecommand=(self._okfct, '%d', '%S'),
                                     validate='key', justify="center")
        self.string_nb_entry.grid(row=0, column=7, sticky="e", padx=(0,5))
        Button(toolbar2, image=self.icon_plus,
               command=self.add_string).grid(row=0, column=8, pady=2, padx=2)
        Button(toolbar2, image=self.icon_moins,
               command=self.del_string).grid(row=0, column=9, pady=2, padx=2)

        # configuration du motif
        self.row_nb = row_nb
        self.string_nb = string_nb

        # canvas
        w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
        self.can = Canvas(motif_frame, borderwidth=2, relief="groove",
                          bg=CANVAS_COLOR, highlightthickness=0,
                          width=min(self.width_max, w),
                          height=min(self.row_nb*22 + 20, self.height_max))
        self.can.grid(row=1, column=0, sticky="wens")
        self.scroll_vert = Scrollbar(motif_frame, command=self.can.yview,
                                     orient="vertical")
        self.scroll_horiz = Scrollbar(motif_frame, command=self.can.xview,
                                      orient="horizontal")
        self.can.configure(yscrollcommand=self.scroll_vert.set)
        self.can.configure(xscrollcommand=self.scroll_horiz.set)
        self.scroll_vert.grid(row=1, column=1, sticky="ns")
        self.scroll_horiz.grid(row=2, sticky="ew")
        self.is_scrollable = True
        self._init_canvas()

        # keybindings
        self.bind("<Control-o>", self.open)
        self.bind("<Control-q>", self.exit)
        self.bind("<Control-s>", self.save)
        self.bind("<Control-Shift-S>", self.saveas)
        self.bind("<Control-g>", self.generate)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-x>", self.clear)
        self.bind("<Control-b>", self.set_bg)
        self.bind("<Control-f>", self.set_fg)
        self.bind("<Control-m>", self.shift_motif)
        self.bind("<Up>", lambda event: self.shift("n"))
        self.bind("<Down>", lambda event: self.shift("s"))
        self.bind("<Right>", lambda event: self.shift("e"))
        self.bind("<Left>", lambda event: self.shift("w"))
        self.bind("<Control-KP_8>", lambda event: self.shift("n"))
        self.bind("<Control-KP_2>", lambda event: self.shift("s"))
        self.bind("<Control-KP_6>", lambda event: self.shift("e"))
        self.bind("<Control-KP_4>", lambda event: self.shift("w"))
        self.bind("<Control-KP_9>", lambda event: self.shift("ne"))
        self.bind("<Control-KP_1>", lambda event: self.shift("sw"))
        self.bind("<Control-KP_3>", lambda event: self.shift("se"))
        self.bind("<Control-KP_7>", lambda event: self.shift("nw"))
        self.bind("<KP_Add>", self.add_row)
        self.bind("<KP_Subtract>", self.del_row)
        self.bind("<Control-KP_Add>", self.add_string)
        self.bind("<Control-KP_Subtract>", self.del_string)
        self.bind("<plus>", self.add_row)
        self.bind("<minus>", self.del_row)
        self.bind("<Control-plus>", self.add_string)
        self.bind("<Control-minus>", self.del_string)
        self.bind("<Control-l>", lambda event: self.rotate("ccw"),
                  add=True)
        self.bind("<Control-r>", lambda event: self.rotate("cw"),
                  add=True)
        self.bind("<Control-v>", lambda event: self.symmetrize("vertical"),
                  add=True)
        self.bind("<Control-h>", lambda event: self.symmetrize("horizontal"),
                  add=True)
        self.bind('<Key-F1>', help)
        self.bind('<Control-Key-F1>', help_web)

        for key in MOUSEWHEEL:
            self.bind(key, self._mouse_scroll)

        self.row_nb_entry.bind("<Return>", self.change_row_nb)
        self.row_nb_entry.bind("<FocusOut>", self.change_row_nb)
        self.string_nb_entry.bind("<Return>", self.change_string_nb)
        self.string_nb_entry.bind("<FocusOut>", self.change_string_nb)

        # informations récupérées à la fermeture de la fenêtre par le
        # programme principal
        self.result = None

        self.is_saved = True
        self.path_save = fichier

        self.focus_set()
        self.is_saved = True

        if fichier:
            self.open(fichier=fichier)
        # self.wait_window(self)

    def about(self):
        """ ouvre la fenêtre 'à propos de Bracelet Generator' """
        About(self)

    def _init_canvas(self):
        """ création du contenu de la fenêtre """

        self.carreaux = []  # id des carreaux du motif
        self.motif = []  # motif: 0 = bg, 1 = fg
        # remplissage du canvas
        for i in range(self.row_nb):
            self.carreaux.append([])
            self.motif.append([])
            if i % 2:  # ligne impaire
                nb_noeuds = self.string_nb//2 - 1 + self.string_nb % 2
                for j in range(nb_noeuds):
                    self.carreaux[i].append(self._carreau(50 + j*40,
                                                          50 + i//2*40))
                    self.motif[i].append(0)
                    self._attribue_carreau(i, j)
            else:  # ligne paire
                nb_noeuds = self.string_nb//2
                for j in range(nb_noeuds):
                    self.carreaux[i].append(self._carreau(30 + j*40,
                                                          30 + i//2*40))
                    self.motif[i].append(0)
                    self._attribue_carreau(i, j)

        self.can.configure(scrollregion=[self.can.bbox('all')[0] - 10,
                                         self.can.bbox('all')[1] - 10,
                                         self.can.bbox('all')[2] + 10,
                                         self.can.bbox('all')[3] + 10])
    def __setattr__(self, name, value):
        """ gestion de la modification attributs, en particulier
            les nombres de fils et de lignes ainsi que la sauvegarde """
        if name == "string_nb":
            self.string_nb_entry.delete(0,"end")
            self.string_nb_entry.insert(0, value)
        elif name == "row_nb":
            self.row_nb_entry.delete(0,"end")
            self.row_nb_entry.insert(0, value)
        elif name == "is_saved":
            dico = {"True":"disabled", "False":"normal"}
            self.save_button.configure(state=dico[str(value)])
            self.menu_file.entryconfigure(3, state=dico[str(value)])

        object.__setattr__(self, name, value)


    def add_recent_file(self, file):
        """ ajoute fichier aux fichiers récents (de l'éditeur de motifs et du logiciel),
            supprime le plus ancien s'il y en a plus de 10,
            actualise le menu des fichiers récents """
        if not RECENT_BICOLOR:
            self.menu_file.entryconfigure(1, state="normal")
        if file in RECENT_BICOLOR:
            i = RECENT_BICOLOR.index(file)
            self.menu_recent_files.delete(i)
            RECENT_BICOLOR.remove(file)

        RECENT_BICOLOR.insert(0, file)
        self.menu_recent_files.insert_command(0,label=file,
                                              command=lambda: self.open(fichier=file))
        if len(RECENT_BICOLOR) > 10:
            self.menu_recent_files.delete(10)
            del(RECENT_BICOLOR[-1])
        self.master.add_recent_file(file)

    def del_recent_file(self, file):
        """ supprime file aux fichiers récents (de l'éditeur de motifs et du logiciel),
            actualise le menu des fichiers récents """
        if file in RECENT_BICOLOR:
            i = RECENT_BICOLOR.index(file)
            self.menu_recent_files.delete(i)
            RECENT_BICOLOR.remove(file)

        self.master.del_recent_file(file)

        if not RECENT_BICOLOR:
            self.menu_file.entryconfigure(1, state="disabled")

    def shift_motif(self, event=None):
        top = Toplevel(self)
        top.transient(self)
        top.title(_("Shift"))
        top.configure(bg=BG_COLOR)
        top.resizable(0,0)
        top.grab_set()
        style = Style(top)
        style.theme_use(STYLE)
        style.configure('TButton', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR)
        style.configure('TFrame', background=BG_COLOR)
        top.icon_move_e = open_image(master=top,file=IM_MOVE_E)
        top.icon_move_s = open_image(master=top,file=IM_MOVE_S)
        top.icon_move_w = open_image(master=top,file=IM_MOVE_W)
        top.icon_move_n = open_image(master=top,file=IM_MOVE_N)
        top.icon_move_se = open_image(master=top,file=IM_MOVE_SE)
        top.icon_move_sw = open_image(master=top,file=IM_MOVE_SW)
        top.icon_move_nw = open_image(master=top,file=IM_MOVE_NW)
        top.icon_move_ne = open_image(master=top,file=IM_MOVE_NE)
        Button(top, image=top.icon_move_nw,
               command=lambda: self.shift("nw")).grid(row=0, column=0)
        Button(top, image=top.icon_move_n,
               command=lambda: self.shift("n")).grid(row=0, column=1)
        Button(top, image=top.icon_move_ne,
               command=lambda: self.shift("ne")).grid(row=0, column=2)
        Button(top, image=top.icon_move_w,
               command=lambda: self.shift("w")).grid(row=1, column=0)
        Label(top, image=self.icon_move).grid(row=1, column=1)
        Button(top, image=top.icon_move_e,
               command=lambda: self.shift("e")).grid(row=1, column=2)
        Button(top, image=top.icon_move_sw,
               command=lambda: self.shift("sw")).grid(row=2, column=0)
        Button(top, image=top.icon_move_s,
               command=lambda: self.shift("s")).grid(row=2, column=1)
        Button(top, image=top.icon_move_se,
               command=lambda: self.shift("se")).grid(row=2, column=2)
        top.bind("<Control-z>", self.undo)
        top.bind("<Control-y>", self.redo)

    def shift(self, direction, write_log=True):
        """ translate le motif
            direction : n, s, e, w, ne, nw, sw, se """
        parite = "pi"[self.string_nb % 2] # pour undo
        if direction == "n":
            self.motif = self.motif[2:] + self.motif[:2]
        elif direction == "s":
            self.motif = self.motif[-2:] + self.motif[:-2]
        elif direction =="e":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            for i in range(len(self.motif)):
                self.motif[i] = self.motif[i][-1:] + self.motif[i][:-1]
        elif direction =="w":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            for i in range(len(self.motif)):
                self.motif[i] = self.motif[i][1:] + self.motif[i][:1]
        elif direction =="se":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            self.motif = self.motif[-1:] + self.motif[:-1]
            for i in range(0,len(self.motif),2):
                self.motif[i] = self.motif[i][-1:] + self.motif[i][:-1]
        elif direction =="ne":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            self.motif = self.motif[1:] + self.motif[:1]
            for i in range(0,len(self.motif),2):
                self.motif[i] = self.motif[i][-1:] + self.motif[i][:-1]
        elif direction =="sw":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            self.motif = self.motif[-1:] + self.motif[:-1]
            for i in range(1,len(self.motif),2):
                self.motif[i] = self.motif[i][1:] + self.motif[i][:1]
        elif direction =="nw":
            if not self.string_nb % 2:
                # nombre pair de fils
                self.add_string(False)
            self.motif = self.motif[1:] + self.motif[:1]
            for i in range(1,len(self.motif),2):
                self.motif[i] = self.motif[i][1:] + self.motif[i][:1]

        for i in range(self.row_nb):
            for j in range(len(self.carreaux[i])):
                self.can.itemconfig(self.carreaux[i][j],
                                    fill=self.colors[self.motif[i][j]])
        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                log.write("shift %s %s\n" % (direction, parite))
        self.is_saved = False


    def rotate(self, sens, write_log=True, instruction="s"):
        """ sens : ccw (counter-clockwise) ou cw (clockwise)
            write_log : écrire ou non dans le fichier log
            (ie s'agit-il d'une action de l'utilisateur ou
            d'une annulation/rétablissment
            instructions : p/i annulation pour un nb initial de fils
            pair/impair """

        for i in range(self.row_nb):
            for c in self.carreaux[i]:
                self.can.delete(c)
        self.carreaux = []
        motif = []
        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                instructions = "pi"
                log.write("rotate %s %s\n" % (sens,
                                                instructions[self.string_nb % 2]))
        if sens == "ccw":
            if self.string_nb % 2:
                self.row_nb, self.string_nb = self.string_nb - 1, self.row_nb + 2
                p = self.string_nb - 1
                for i in range(self.row_nb):
                    motif.append([])
                    if i % 2 == 0:
                        motif[i].append(0)
                    for j in range(p//2):
                        motif[i].append(self.motif[2*j + 1 - i % 2]
                                        [(self.row_nb - 1 - i)//2])

            else:
                self.string_nb, self.row_nb = self.row_nb + 1, self.string_nb
                for i in range(self.row_nb - 1):
                    motif.append([])
                    for j in range(self.string_nb//2):
                        motif[i].append(self.motif[2*j + i % 2]
                                        [(self.row_nb - 2 - i)//2])
                if instruction == "s":
                    motif.append([0]*(self.string_nb//2))
                else:
                    motif = motif[:-1]
                    self.row_nb -= 2
                    if instruction == "p":
                        for i in range(1, self.row_nb, 2):
                            motif[i] = motif[i][:-1]
                        self.string_nb -= 1

        else:
            if self.string_nb % 2:
                self.row_nb, self.string_nb = self.string_nb - 1, self.row_nb + 2
                p = (self.string_nb - 1)//2
                for i in range(self.row_nb):
                    motif.append([])
                    if i % 2 == 0 and instruction != "p":
                        motif[i].append(0)
                    for j in range(p):
                        motif[i].append(self.motif[(p - 1 - j)*2 + i % 2][i//2])
                if instruction == "p":
                    self.string_nb -= 2
                    for i in range(1, self.row_nb, 2):
                        motif[i] = motif[i][1:]
            else:
                self.string_nb, self.row_nb = self.row_nb + 2, self.string_nb
                p = (self.string_nb - 1)//2
                for i in range(self.row_nb - 1):
                    motif.append([])
                    if i % 2 == 0:
                        motif[i].append(0)
                    for j in range(p):
                        motif[i].append(self.motif[(p - 1 - j)*2 + i % 2]
                                        [i//2])
                if instruction != "i":
                    motif.append([0]*((self.string_nb - 1)//2))
                elif instruction == "i":
                    self.row_nb -= 2
                    self.string_nb -= 1
                    motif = motif[1:]
                    for i in range(1, self.row_nb, 2):
                        motif[i] = motif[i][1:]
        self.motif = motif

        for i in range(self.row_nb):
            self.carreaux.append([])
            if i % 2:  # ligne impaire
                for j, coul in enumerate(self.motif[i]):
                    self.carreaux[i].append(self._carreau(50 + j*40,
                                                          50 + i//2*40,
                                                          fill=self.colors[coul]))
                    self._attribue_carreau(i, j)
            else:
                for j, coul in enumerate(self.motif[i]):
                    self.carreaux[i].append(self._carreau(30 + j*40,
                                                          30 + i//2*40,
                                                          fill=self.colors[coul]))
                    self._attribue_carreau(i, j)
        self.is_saved = False
        w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
        h = 50 + (self.row_nb//2)*40
        self.can.configure(width=min(self.width_max, w),
                           height=min(h, self.height_max),
                           scrollregion=[self.can.bbox('all')[0] - 10,
                                         self.can.bbox('all')[1] - 10,
                                         self.can.bbox('all')[2] + 10,
                                         self.can.bbox('all')[3] + 10])




    def symmetrize(self, sens, write_log=True):
        """ symétrise le motif verticalement ou horizontalement """

        if sens == "horizontal":
            n = self.string_nb//2 - 1
            if self.string_nb % 2:
                for i in range(self.row_nb):
                    for k, j in enumerate(range(n - i % 2, - 1, - 1)):
                        coul = self.motif[i][j]
                        self.motif[i].append(coul)
                        self.carreaux[i].append(self._carreau(30 + 20*(i % 2)
                                                              + (n + 1 + k)*40,
                                                              30 + 20*(i % 2) + i//2*40,
                                                              self.colors[coul]))
                        self._attribue_carreau(i, n + 1 + k)

            else:
                for i in range(self.row_nb):
                    for k, j in enumerate(range(n - 1, - 1, - 1)):
                        coul = self.motif[i][j]
                        self.motif[i].append(coul)
                        self.carreaux[i].append(self._carreau(30 + 20*(i % 2) +
                                                              (n + 1 + k -
                                                               (i % 2))*40,
                                                              30 + 20*(i % 2)
                                                              + i//2*40,
                                                              self.colors[coul]))
                        self._attribue_carreau(i, n + 1 + k - i % 2)

            self.string_nb = (self.string_nb - 1)*2


        else:
            row_nb = self.row_nb*2 - 1
            for k, i in zip(range(self.row_nb, row_nb),
                            range(self.row_nb - 2, -1, -1)):
                self.motif.append([])
                self.carreaux.append([])
                for j, coul in enumerate(self.motif[i]):
                    self.motif[k].append(coul)
                    self.carreaux[k].append(self._carreau(30 + 20*(k % 2) + j*40,
                                                          30 + 20*(k % 2) +
                                                          k//2*40,
                                                          self.colors[coul]))
                    self._attribue_carreau(k, j)
            self.motif.append([])
            self.carreaux.append([])
            for j in range(self.string_nb//2 - 1 + self.string_nb % 2):
                self.motif[row_nb].append(0)
                self.carreaux[row_nb].append(self._carreau(50 + j*40,
                                                              50 + row_nb//2*40,
                                                              self.colors[0]))
                self._attribue_carreau(row_nb, j)

            self.row_nb = row_nb + 1


        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                log.write("symmetrize %s\n" % (sens))

        w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
        h = 50 + (self.row_nb//2)*40
        self.can.configure(width=min(self.width_max, w),
                           height=min(h, self.height_max),
                           scrollregion=[self.can.bbox('all')[0] - 10,
                                         self.can.bbox('all')[1] - 10,
                                         self.can.bbox('all')[2] + 10,
                                         self.can.bbox('all')[3] + 10])

        self.is_saved = False

    def open(self, event=None, fichier=""):
        """ ouvre un motif contenu dans un fichier .motif """
        rep = False
        if not self.is_saved:
            rep = askyesnocancel('Question', "The motif has not been saved. \
                                              Do you want to save it before \
                                              replacing it with another one?",
                                 icon="warning", parent=self)
            if rep:
                self.save()
        if rep is not None:
            if not fichier:
                fichier = askopenfilename(defaultextension='.bicolor',
                                          filetypes=[('BICOLOR', '*.bicolor')],
                                          parent=self, initialdir=CONFIG.get("General", "last_path"))
            if fichier:
                if os.path.exists(fichier):
                    CONFIG.set("General", "last_path", os.path.dirname(fichier))
                    self.add_recent_file(fichier)
                    if fichier.split(".")[-1] == "bicolor":
                        for i in range(self.row_nb):
                            for c in self.carreaux[i]:
                                self.can.delete(c)
                        self.carreaux = []
                        with open(fichier, "rb") as fich:
                            dp = Unpickler(fich)
                            self.row_nb = dp.load()
                            self.string_nb = dp.load()
                            self.colors = dp.load()
                            self.motif = dp.load()
                            fill(self.icon_bg, self.colors[0])
                            fill(self.icon_fg, self.colors[1])
    #                        self.b_bg.configure(image=self.icon_bg)
    #                        self.b_fg.configure(image=self.icon_fg)
                            for i in range(self.row_nb):
                                self.carreaux.append([])
                                if i % 2:  # ligne impaire
                                    for j, coul in enumerate(self.motif[i]):
                                        self.carreaux[i].append(self._carreau(50 + j*40,
                                                                              50 + i//2*40,
                                                                              fill=self.colors[coul]))
                                        self._attribue_carreau(i, j)
                                else:
                                    for j, coul in enumerate(self.motif[i]):
                                        self.carreaux[i].append(self._carreau(30 + j*40,
                                                                              30 + i//2*40,
                                                                              fill=self.colors[coul]))
                                        self._attribue_carreau(i, j)
                            self.path_save = fichier
                            self._logreset()
                            self.is_saved = True
                            w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
                            h = 50 + (self.row_nb//2)*40
                            self.can.configure(width=min(self.width_max, w),
                                               height=min(h, self.height_max),
                                               scrollregion=[self.can.bbox('all')[0] - 10,
                                                             self.can.bbox('all')[1] - 10,
                                                             self.can.bbox('all')[2] + 10,
                                                             self.can.bbox('all')[3] + 10])



                    else:  # il y a eu une erreur
                        showerror(_("Error"),
                                  _("The file %(name)s is not a valid two-colored motif file.") % ({"name": os.path.split(fichier)[-1]}),
                                  parent=self)
                else:
                    showerror(_("Error"),
                              _("The file %(name)s does not exists.") % ({"name": fichier}),
                             parent=self)
                    self.del_recent_file(fichier)

    def clear(self, event=None):
        """ remet tous les carreaux à la color de l'arrière plan """
        rep = askyesno("Question",
                       _("Do you really want to clear the motif?"),
                       parent=self)
        if rep:
            for i in range(self.row_nb):
                for j in range(len(self.carreaux[i])):
                    self.can.itemconfig(self.carreaux[i][j],
                                        fill=self.colors[0])
                    self.motif[i][j] = 0
        self._logreset()

    def save(self, event=None, fichier=None):
        """ enregistre le motif """
        if not self.is_saved:
            if fichier is None and not self.path_save:
                self.saveas()
            else:
                if fichier is None:
                    fichier = self.path_save
                with open(fichier, "wb") as fich:
                    p = Pickler(fich)
                    p.dump(self.row_nb)
                    p.dump(self.string_nb)
                    p.dump(self.colors)
                    p.dump(self.motif)
                self.is_saved = True

    def saveas(self, event=None):
        """ demande le chemin d'enregistrement puis enregistre le motif
            (fct enregistrer sous) """
        if self.path_save:
            initialdir, initialfile = os.path.split(self.path_save)
        else:
            initialdir=CONFIG.get("General", "last_path")
            initialfile=""
        fichier = asksaveasfilename(defaultextension='.bicolor',
                                    parent=self,
                                    filetypes=[('BICOLOR', '*.bicolor')],
                                    initialdir=initialdir,
                                    initialfile=initialfile)
        if fichier:
            self.add_recent_file(file=fichier)
            CONFIG.set("General", "last_path", os.path.dirname(fichier))
            ext = fichier.split(".")[-1]
            if ext == "bicolor":
                self.save(fichier=fichier)
                self.path_save = fichier
            else:
                showerror(_("Error"),
                          _(".%(extension)s is not a valid extension for a two-colored motif file.") % ({"extension": ext}),
                          parent=self)

    def undo(self, event=None):
        """ annule la dernière action """
        if self.log_ligne > 1:
            with open(BICOLOR_LOG, "r") as log:
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
            elif txt[0] == "fg":
                self.set_fg(write_log=False, fg=txt[1])
            elif txt[0] == "bg":
                self.set_bg(write_log=False, bg=txt[1])
            elif txt[0] == "clic_carreau":
                self._clic_carreau(int(txt[1]), int(txt[2]), write_log=False)
            elif txt[0] == "del_string":
                self.add_string(write_log=False, motif=txt[1])
            elif txt[0] == "del_row":
                self.add_row(write_log=False, motif=(txt[1], txt[2]))
            elif txt[0] == "rotate":
                inverse_sens = dict(ccw="cw", cw="ccw")
                self.rotate(inverse_sens[txt[1]], False, txt[2])
            elif txt[0] == "shift":
                inverse = dict(n="s", s="n", w="e", e="w",
                               sw="ne", ne="sw", se="nw", nw="se")
                self.shift(inverse[txt[1]], write_log=False)
                if txt[1] in ["e", "w"] and txt[2] == "p":
                    self.del_string(write_log=False)

            elif txt[0] == "symmetrize":
                if txt[1] == "horizontal":
                    n = self.string_nb//2
                    for i in range(self.string_nb - n + 1, self.string_nb):
                        self.del_string(write_log=False)
                elif txt[1] == "vertical":
                    l = self.row_nb//2
                    for i in range(l//2):
                        self.del_row(write_log=False)

    def redo(self, event=None):
        """ rétablit la dernière action annulée """
        if self.log_ligne < self.log_nb_ligne - 1:
            with open(BICOLOR_LOG, "r") as log:
                logfile = log.readlines()
            self.log_ligne += 1
            if self.log_ligne == self.log_nb_ligne - 1:
                self.menu_edit.entryconfigure(1, state="disabled")
            txt = logfile[self.log_ligne].split()
            if txt[0] == "add_string":
                self.add_string(write_log=False)
            elif txt[0] == "add_row":
                self.add_row(write_log=False)
            elif txt[0] == "fg":
                self.set_fg(write_log=False, fg=txt[2])
            elif txt[0] == "bg":
                self.set_bg(write_log=False, bg=txt[2])
            elif txt[0] == "clic_carreau":
                self._clic_carreau(int(txt[1]), int(txt[2]), False)
            elif txt[0] == "del_string":
                self.del_string(write_log=False)
            elif txt[0] == "del_row":
                self.del_row(write_log=False)
            elif txt[0] == "rotate":
                self.rotate(txt[1], write_log=False)
            elif txt[0] == "shift":
                self.shift(txt[1], write_log=False)
            elif txt[0] == "symmetrize":
                self.symmetrize(txt[1], False)

    def _logreset(self):
        """ réinitialise le fichier log
            ie efface l'historique des actions effectuées """
        with open(BICOLOR_LOG, "w") as log:
            log.write("#Bracelet Generator Bicolor logfile\n\n")
        self.log_ligne = 1  # ligne actuelle dans le fichier log
        self.log_nb_ligne = 2  # nombre de lignes du fichier log
        self.menu_edit.entryconfigure(0, state="disabled")
        self.menu_edit.entryconfigure(1, state="disabled")

    def _log(self):
        """ annule la possibilté de faire redo une fois qu'on a remodifié
            le bracelet """
        self.log_nb_ligne += 1
        self.log_ligne += 1
        self.menu_edit.entryconfigure(0, state="normal")
        if self.log_ligne != self.log_nb_ligne - 1:
            self.menu_edit.entryconfigure(1, state="disabled")
            with open(BICOLOR_LOG, "r") as log:
                logfile = log.readlines()
            with open(BICOLOR_LOG, "w") as log:
                # supprime les actions annulées précédemment
                for ligne in logfile[:self.log_ligne]:
                    log.write(ligne)
            self.log_nb_ligne = self.log_ligne + 1

    def generate(self, event=None):
        """ génère le bracelet correspondant au motif
            ie met les infos sur le motif dans self.result et ferme
            la fenêtre pour que le programme principal reprenne la main. """
        rep = False
        if not self.is_saved:
            rep = askyesnocancel('Question',
                                 _("The two-colored motif has not been saved. Do you want to save it before generating the pattern?"),
                                 parent=self)
        if rep is not None:
            if rep:
                self.save()
            motif = []
            for i in range(self.row_nb):
                motif.append([])
                for c in self.carreaux[i]:
                    motif[i].append(int(self.can.itemcget(c, "fill") ==
                                        self.colors[1]))
            self.withdraw()
            self.update_idletasks()
            if self.master:
                self.master.focus_set()

            self.result = self.row_nb, self.string_nb, self.colors, motif

            if os.path.exists(BICOLOR_LOG):
                os.remove(BICOLOR_LOG)
            save_config()
            self.destroy()

    def _mouse_scroll(self, event):
        """ défilement vertical du canvas grâce à la molette de la souris """
        if self.is_scrollable:
            self.can.yview_scroll(mouse_wheel(event), "units")

    def set_bg(self, event=None, write_log=True, bg=None):
        """ change la color du fond """
        if bg is None:
            bg = askcolor(self.colors[0], parent=self, title=_("Background Color"))
        if bg:
            if write_log:
                self._log()
                with open(BICOLOR_LOG, "a") as log:
                    log.write("bg %s %s\n" % (self.colors[0], bg))
            self.colors[0] = bg
            fill(self.icon_bg, self.colors[0])
            self.b_bg.configure(image=self.icon_bg)
            fill(self.m_bg, self.colors[0])

            for i in range(self.row_nb):
                for c, coul in zip(self.carreaux[i], self.motif[i]):
                    if coul == 0:
                        self.can.itemconfig(c, fill=self.colors[0])
            self.is_saved = False

    def set_fg(self, event=None, write_log=True, fg=None):
        """ change la color du motif """
        if fg is None:
            fg = askcolor(self.colors[1], parent=self, title=_("Foreground Color"))
        if fg:
            if write_log:
                self._log()
                with open(BICOLOR_LOG, "a") as log:
                    log.write("fg %s %s\n" % (self.colors[1], fg))
            self.colors[1] = fg
            fill(self.icon_fg, self.colors[1])
            self.b_fg.configure(image=self.icon_fg)
            fill(self.m_fg, self.colors[1])
            for i in range(self.row_nb):
                for c, coul in zip(self.carreaux[i], self.motif[i]):
                    if coul == 1:
                        self.can.itemconfig(c, fill=self.colors[1])
            self.is_saved = False

    def _attribue_carreau(self, i, j):
        """ astuce pour réaliser les tag_bind dans une boucle """
        self.can.tag_bind(self.carreaux[i][j], '<Button - 1>',
                          lambda event: self._clic_carreau(i, j))

    def _clic_carreau(self, i, j, write_log=True):
        """ action lorsqu'on clique sur un carreau: changement de sa color"""
        self.focus_set()
        color = (self.motif[i][j] + 1) % 2
        self.can.itemconfig(self.carreaux[i][j], fill=self.colors[color])
        self.motif[i][j] = color
        self.is_saved = False
        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                log.write("clic_carreau %i %i\n" % (i, j))

    def _carreau(self, x, y, fill=None):
        """ dessine un _carreau de centre (x, y) et de 'rayon' 20 sur le canvas
            renvoie l'id du _carreau """
        if fill is None:
            fill = self.colors[0]
        return self.can.create_polygon(x, y - 20, x + 20, y, x, y + 20,
                                       x - 20, y, fill=fill, outline='black')

    def exit(self, event=None):
        """ demande si l'on veut enregistrer et quitte """
        if not self.is_saved:
            rep = askyesnocancel('Question',
                                 _("The two-colored motif has not been saved. Do you want to save it before closing?"),
                                 parent=self)
            if rep is not None:
                if rep:
                    self.save()
                if self.master:
                    self.master.focus_set()
                if os.path.exists(BICOLOR_LOG):
                    os.remove(BICOLOR_LOG)
                save_config()
                self.destroy()
                return True
            else:
                return False
        else:
            if self.master:
                self.master.focus_set()
            if os.path.exists(BICOLOR_LOG):
                os.remove(BICOLOR_LOG)
            save_config()
            self.destroy()
            return True

    def change_row_nb(self, event=None):
        ch = self.row_nb_entry.get()
        if ch:
            nb = int(ch)
            if nb >= 2:
                diff = nb - self.row_nb
                if diff > 0:
                    for i in range(diff//2):
                        self.add_row()
                elif diff < 0:
                    for i in range((-diff)//2):
                        self.del_row()
        self.row_nb = self.row_nb
        self.focus_set()

    def add_row(self, event=None, write_log=True, motif=None):
        """ rajoute 2 lignes """
        i = self.row_nb
        self.row_nb += 2
        self.carreaux.append([])
        self.motif.append([])
        nb_noeuds = self.string_nb//2
        if motif is None:
            motif = ["0"*nb_noeuds, "0"*(nb_noeuds - 1 + self.string_nb % 2)]
        for j in range(nb_noeuds):
            coul = int(motif[0][j])
            self.carreaux[i].append(self._carreau(30 + j*40, 30 + i//2*40,
                                                  self.colors[coul]))
            self.motif[i].append(coul)
            self._attribue_carreau(i, j)
        self.carreaux.append([])
        self.motif.append([])
        i += 1
        nb_noeuds = self.string_nb//2 - 1 + self.string_nb % 2
        for j in range(nb_noeuds):
            coul = int(motif[1][j])
            self.carreaux[i].append(self._carreau(50 + j*40,
                                                  50 + i//2*40,
                                                  self.colors[coul]))
            self.motif[i].append(coul)
            self._attribue_carreau(i, j)
        h = 50 + (self.row_nb//2)*40
        self.can.config(height=min(h, self.height_max),
                        scrollregion=[self.can.bbox('all')[0] - 10,
                                      self.can.bbox('all')[1] - 10,
                                      self.can.bbox('all')[2] + 10,
                                      self.can.bbox('all')[3] + 10])
        self.is_saved = False

        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                log.write("add_row\n")

    def del_row(self, event=None, write_log=True):
        """ efface deux lignes """
        if self.row_nb > 2:
            motif = ""
            for b, c in zip(self.motif[-2], self.carreaux[-2]):
                motif += str(b)
                self.can.delete(c)
            motif += " "
            for b, c in zip(self.motif[-1], self.carreaux[-1]):
                motif += str(b)
                self.can.delete(c)

            self.carreaux = self.carreaux[:-2]
            self.motif = self.motif[:-2]
            self.row_nb -= 2
            h = 50 + (self.row_nb//2)*40
            self.can.configure(height=min(h, self.height_max),
                               scrollregion=[self.can.bbox('all')[0] - 10,
                                             self.can.bbox('all')[1] - 10,
                                             self.can.bbox('all')[2] + 10,
                                             self.can.bbox('all')[3] + 10])
            self.is_saved = False

            if write_log:
                self._log()
                with open(BICOLOR_LOG, "a") as log:
                    log.write("del_row %s\n" % (motif))

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

    def add_string(self, event=None, write_log=True, motif=None):
        """ ajoute un fil au bracelet"""
        if motif is None:
            motif = "0"*(self.row_nb//2)
        self.string_nb += 1
        nb = self.string_nb//2 - 1

        if self.string_nb % 2:
            for i in range(1, self.row_nb, 2):
                coul = int(motif[i//2])
                self.carreaux[i].append(self._carreau(50 + nb*40,
                                                      50 + i//2*40,
                                                      self.colors[coul]))
                self.motif[i].append(coul)
                self._attribue_carreau(i, nb)
        else:
            for i in range(0, self.row_nb, 2):
                coul = int(motif[i//2])
                self.carreaux[i].append(self._carreau(30 + nb*40,
                                                      30 + i//2*40,
                                                      self.colors[coul]))
                self.motif[i].append(coul)
                self._attribue_carreau(i, nb)
        w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
        self.can.configure(width=min(self.width_max, w),
                           scrollregion=[self.can.bbox('all')[0] - 10,
                                         self.can.bbox('all')[1] - 10,
                                         self.can.bbox('all')[2] + 10,
                                         self.can.bbox('all')[3] + 10])

        self.is_saved = False

        if write_log:
            self._log()
            with open(BICOLOR_LOG, "a") as log:
                log.write("add_string\n")

    def del_string(self, event=None, write_log=True):
        """ efface un fil """
        if self.string_nb > 3:
            motif = ""
            self.string_nb -= 1
            for i in range((self.string_nb - 1) % 2, self.row_nb, 2):
                motif += str(self.motif[i][-1])
                self.can.delete(self.carreaux[i][-1])
                self.carreaux[i] = self.carreaux[i][:-1]
                self.motif[i] = self.motif[i][:-1]
            w = 30 + (self.string_nb//2)*40 + (self.string_nb % 2)*20
            self.can.configure(width=min(self.width_max, w),
                               scrollregion=[self.can.bbox('all')[0] - 10,
                                             self.can.bbox('all')[1] - 10,
                                             self.can.bbox('all')[2] + 10,
                                             self.can.bbox('all')[3] + 10])

            self.is_saved = False

            if write_log:
                self._log()
                with open(BICOLOR_LOG, "a") as log:
                    log.write("del_string %s\n" % (motif))

    def get_result(self):
        """renvoie le résultat """
        return self.result
