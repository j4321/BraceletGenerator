#! /usr/bin/python3
# -*- coding:Utf-8 -*-
"""
Bracelet Generator - An easy way to design friendship bracelet patterns
Copyright 2014-2016 Juliette Monsel <j_4321@sfr.fr>

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


Constants and global functions of Bracelet Generator
"""

VERSION = "1.3.2"

STYLE = 'clam'

from locale import getdefaultlocale
import os
from tkinter import TclVersion
from sys import platform
import gettext
from configparser import ConfigParser
from webbrowser import open as webOpen
from subprocess import  check_output, CalledProcessError

PL = os.name

from tkinter import filedialog
from tkinter import colorchooser

# Traduction

APP_NAME = "BraceletGenerator"

# Get the local directory since we are not installing anything
PATH = os.path.split(__file__)[0]
LOCAL_PATH = os.path.expanduser("~")
LOCAL_PATH = os.path.join(LOCAL_PATH, "BraceletGenerator")
if not os.path.exists(LOCAL_PATH):
    os.mkdir(LOCAL_PATH)

PATH_CONFIG = os.path.join(LOCAL_PATH, 'BraceletGenerator.ini')

IMAGES_LOCATION = os.path.join(PATH, 'images')

PATH_LOCALE = os.path.join(PATH, "locale")

PATH_DOC = os.path.join(PATH, "doc")

# lecture du fichier de configuration
CONFIG = ConfigParser()
if os.path.exists(PATH_CONFIG):
    CONFIG.read(PATH_CONFIG)
    LANGUE = CONFIG.get("General","language")
else:
    LANGUE = ""
    CONFIG.add_section("General")
    CONFIG.set("General", "last_path", LOCAL_PATH)
    CONFIG.set("General", "recent_files", "")
    CONFIG.set("General", "recent_bicolor", "")
    CONFIG.set("General", "language", "en")

    CONFIG.add_section("Bracelet")
    CONFIG.set("Bracelet", "row_nb", "4")
    CONFIG.set("Bracelet", "string_nb", "4")
    CONFIG.set("Bracelet", "default_color", "#ff0000")

if LANGUE not in ["en", "fr"]:
    # Check the default locale
    lc = getdefaultlocale()[0][:2]
    if lc == "fr":
        # If we have a default, it's the first in the list
        LANGUE = "fr_FR"
    else:
        LANGUE = "en_US"
    CONFIG.set("General", "language", LANGUE[:2])

gettext.find(APP_NAME, PATH_LOCALE)
gettext.bind_textdomain_codeset(APP_NAME, "UTF-8")
gettext.bindtextdomain(APP_NAME, PATH_LOCALE)
gettext.textdomain(APP_NAME)
lang = gettext.translation(APP_NAME, PATH_LOCALE,
                           languages=[LANGUE], fallback=True)
_ = lang.gettext


RECENT_FILES = CONFIG.get("General", "recent_files").split(",")
if RECENT_FILES == [""]:
    RECENT_FILES = []
RECENT_BICOLOR = CONFIG.get("General", "recent_bicolor").split(",")
if RECENT_BICOLOR == [""]:
    RECENT_BICOLOR = []

# chemins des images
IM_EXIT_M = os.path.join(IMAGES_LOCATION, "exit_m.png")
IM_EXIT = os.path.join(IMAGES_LOCATION, "exit.png")
IM_EXPORT_M = os.path.join(IMAGES_LOCATION, "export_m.png")
IM_EXPORT = os.path.join(IMAGES_LOCATION, "export.png")
IM_NEW_M = os.path.join(IMAGES_LOCATION, "new_m.png")
IM_NEW = os.path.join(IMAGES_LOCATION, "new.png")
IM_OUVRIR_M = os.path.join(IMAGES_LOCATION, "ouvrir_m.png")
IM_OUVRIR = os.path.join(IMAGES_LOCATION, "ouvrir.png")
IM_SAVEAS_M = os.path.join(IMAGES_LOCATION, "saveas_m.png")
IM_SAVEAS = os.path.join(IMAGES_LOCATION, "saveas.png")
IM_SAUVER_M = os.path.join(IMAGES_LOCATION, "sauver_m.png")
IM_SAUVER = os.path.join(IMAGES_LOCATION, "sauver.png")
IM_UNDO = os.path.join(IMAGES_LOCATION, "undo.png")
IM_REDO = os.path.join(IMAGES_LOCATION, "redo.png")
IM_BICOLORE_M = os.path.join(IMAGES_LOCATION, "bicolore_m.png")
IM_BICOLORE = os.path.join(IMAGES_LOCATION, "bicolore.png")
IM_AIDE = os.path.join(IMAGES_LOCATION, "aide.png")
IM_ABOUT = os.path.join(IMAGES_LOCATION, "about.png")
IM_PLUS = os.path.join(IMAGES_LOCATION, "plus.png")
IM_MOINS = os.path.join(IMAGES_LOCATION, "moins.png")
IM_PLUS_M = os.path.join(IMAGES_LOCATION, "plus_m.png")
IM_MOINS_M = os.path.join(IMAGES_LOCATION, "moins_m.png")
IM_EFFACE = os.path.join(IMAGES_LOCATION, "efface.png")
IM_EFFACE_M = os.path.join(IMAGES_LOCATION, "efface_m.png")
IM_COLOR = os.path.join(IMAGES_LOCATION, "color.png")
IM_COLOR_M = os.path.join(IMAGES_LOCATION, "color_m.png")
IM_MOVE_E = os.path.join(IMAGES_LOCATION, "move_e.png")
IM_MOVE_W = os.path.join(IMAGES_LOCATION, "move_w.png")
IM_MOVE_N = os.path.join(IMAGES_LOCATION, "move_n.png")
IM_MOVE_S = os.path.join(IMAGES_LOCATION, "move_s.png")
IM_MOVE_SE = os.path.join(IMAGES_LOCATION, "move_se.png")
IM_MOVE_NW = os.path.join(IMAGES_LOCATION, "move_nw.png")
IM_MOVE_NE = os.path.join(IMAGES_LOCATION, "move_ne.png")
IM_MOVE_SW = os.path.join(IMAGES_LOCATION, "move_sw.png")
IM_MOVE_E_M = os.path.join(IMAGES_LOCATION, "move_e_m.png")
IM_MOVE_W_M = os.path.join(IMAGES_LOCATION, "move_w_m.png")
IM_MOVE_N_M = os.path.join(IMAGES_LOCATION, "move_n_m.png")
IM_MOVE_S_M = os.path.join(IMAGES_LOCATION, "move_s_m.png")
IM_MOVE_SE_M = os.path.join(IMAGES_LOCATION, "move_se_m.png")
IM_MOVE_NW_M = os.path.join(IMAGES_LOCATION, "move_nw_m.png")
IM_MOVE_NE_M = os.path.join(IMAGES_LOCATION, "move_ne_m.png")
IM_MOVE_SW_M = os.path.join(IMAGES_LOCATION, "move_sw_m.png")
IM_MOVE = os.path.join(IMAGES_LOCATION, "move.png")
IM_MOVE_M = os.path.join(IMAGES_LOCATION, "move_m.png")
IM_ICON48 = os.path.join(IMAGES_LOCATION, "icon48.png")
IM_ICON16 = os.path.join(IMAGES_LOCATION, "icon16.png")
IM_ICON_WIN = os.path.join(IMAGES_LOCATION, "icon.ico")
IM_ROTATION_GCHE = os.path.join(IMAGES_LOCATION, "rotation_gche.png")
IM_ROTATION_DTE = os.path.join(IMAGES_LOCATION, "rotation_dte.png")
IM_ROTATION_GCHE_M = os.path.join(IMAGES_LOCATION, "rotation_gche_m.png")
IM_ROTATION_DTE_M = os.path.join(IMAGES_LOCATION, "rotation_dte_m.png")
IM_SYM_HORIZ = os.path.join(IMAGES_LOCATION, "sym_horizontal.png")
IM_SYM_VERT = os.path.join(IMAGES_LOCATION, "sym_vertical.png")
IM_SYM_HORIZ_M = os.path.join(IMAGES_LOCATION, "sym_horizontal_m.png")
IM_SYM_VERT_M = os.path.join(IMAGES_LOCATION, "sym_vertical_m.png")


if platform == 'darwin' or PL == 'nt':
    BG_COLOR = '#F0F0F0'
    CANVAS_COLOR = "#ffffff"
else:
    BG_COLOR = '#cecece'
    CANVAS_COLOR = '#E8E8E8'
   
    
# platform dependent mouse events
if PL == "nt":
    def mouse_wheel(event):
        """ gestion de la molette de la souris sous windows """
        return - 1*(event.delta//120)
    MOUSEWHEEL = ["<MouseWheel>"]
    RIGHT_CLICK = '<Button-3>'
elif platform == "darwin":
    def mouse_wheel(event):
        """ gestion de la molette de la souris """
        return - 1*(event.delta)
    MOUSEWHEEL = ["<MouseWheel>"]
    RIGHT_CLICK = '<Button-2>'
else:
    def mouse_wheel(event):
        """ gestion de la molette de la souris sous linux """
        if event.num == 5:
            return 1
        elif event.num == 4:
            return - 1
    MOUSEWHEEL = ["<Button - 4>", "<Button - 5>"]
    RIGHT_CLICK = '<Button-3>'

    

def save_config():
    """ sauvegarde du dictionnaire contenant la configuration du logiciel (langue ...) """
    CONFIG.set("General", "recent_files", ",".join(RECENT_FILES))
    CONFIG.set("General", "recent_bicolor", ",".join(RECENT_BICOLOR))
    with open(PATH_CONFIG, 'w') as fichier:
        CONFIG.write(fichier)

def help(event=None):
    """ ouvre l'aide en .html dans la langue de l'interface """
    if LANGUE[:2] == "fr":
        webOpen(os.path.join(PATH_DOC, "doc_fr.html"))
    else:
        webOpen(os.path.join(PATH_DOC, "doc.html"))


def help_web(event=None):
    """ ouvre l'aide en ligne dans la langue de l'interface """
    if LANGUE[:2] == "fr":
        webOpen("http://braceletgenerator.sourceforge.net/index_fr.html")
    else:
        webOpen("http://braceletgenerator.sourceforge.net/")

if TclVersion < 8.6:
    # then tkinter cannot import PNG files directly, we need to use PIL
    from PIL import ImageTk
    from tkinter.messagebox import showinfo
    showinfo(_("Information"), _("This software has been developped using Tcl/Tk 8.6, but you are using an older version. Therefore there might be errors and the images will have a poor quality. Please consider upgrading your Tcl/Tk version."))
    def open_image(file, master=None):
        return ImageTk.PhotoImage(file=file, master=master)
else:
    # no need of ImageTk dependency
    from tkinter import PhotoImage
    def open_image(file, master=None):
        return PhotoImage(file=file, master=master)

def set_icon(fen):
    """ icône de l'application """
    if PL == 'nt':
        fen.iconbitmap(IM_ICON_WIN, default=IM_ICON_WIN)
    else:
        icon = open_image(file=IM_ICON16, master=fen)
        fen.iconphoto(True, icon)


def active_color(color):
    """ pâlit la color (en format hexadécimal "#000000") """
    coul = color[1:]
    rouge = int(coul[:2], 16)
    vert = int(coul[2:4], 16)
    bleu = int(coul[4:], 16)
    if bleu > rouge:
        rouge2 = min(rouge + 40, 255)
        if bleu > vert:
            vert2 = min(vert + 40, 255)
            bleu2 = bleu
        else:
            bleu2 = min(bleu + 40, 255)
            vert2 = vert
    elif rouge > bleu:
        bleu2 = min(bleu + 40, 255)
        if rouge > vert:
            vert2 = min(vert + 40, 255)
            rouge2 = rouge
        else:
            rouge2 = min(rouge + 40, 255)
            vert2 = vert
    elif vert > bleu:
        vert2 = vert
        bleu2 = min(bleu + 40, 255)
        rouge2 = min(rouge + 40, 255)
    elif vert < bleu:
        vert2 = min(vert + 40, 255)
        bleu2 = bleu
        rouge2 = min(rouge + 40, 255)
    else:  # rouge = vert = bleu
        rouge2 = min(rouge + 40, 255)
        vert2 = rouge2
        bleu2 = rouge2
    return "#" + hex(rouge2)[2:] + hex(vert2)[2:] + hex(bleu2)[2:]

def fill(image, color):
     """Fill image with a color=#hex."""
     width = image.width()
     height = image.height()
     horizontal_line = "{" + " ".join([color]*width) + "}"
     image.put(" ".join([horizontal_line]*height))

ZENITY = False
if PL != "nt":
    paths = os.environ['PATH'].split(":")
    for path in paths:
        if os.path.exists(os.path.join(path, "zenity")):
            ZENITY = True

def askopenfilename(defaultextension, filetypes, initialdir, initialfile="", title=_('Open'), **options):
    """ plateform specific file browser:
            - defaultextension: extension added if none is given
            - initialdir: directory where the filebrowser is opened
            - filetypes: [('NOM', '*.ext'), ...]
    """
    if ZENITY:
        try:
            args = ["zenity", "--file-selection",
                    "--filename", os.path.join(initialdir, initialfile)]
            for ext in filetypes:
                args += ["--file-filter", "%s|%s" % ext]
            args += ["--title", title]
            file = check_output(args).decode("utf-8").strip()
            filename, ext = os.path.splitext(file)
            if not ext:
                ext = defaultextension
            return filename + ext
        except CalledProcessError:
            return ""
        except Exception:
            return filedialog.askopenfilename(title=title,
                                              defaultextension=defaultextension,
                                              filetypes=filetypes,
                                              initialdir=initialdir,
                                              initialfile=initialfile,
                                              **options)
    else:
        return filedialog.askopenfilename(title=title,
                                          defaultextension=defaultextension,
                                          filetypes=filetypes,
                                          initialdir=initialdir,
                                          initialfile=initialfile,
                                          **options)

def asksaveasfilename(defaultextension, filetypes, initialdir=".", initialfile="", title=_('Save As'), **options):
    """ plateform specific file browser for saving a file:
            - defaultextension: extension added if none is given
            - initialdir: directory where the filebrowser is opened
            - filetypes: [('NOM', '*.ext'), ...]
    """
    if ZENITY:
        try:
            args = ["zenity", "--file-selection",
                    "--filename", os.path.join(initialdir, initialfile),
                    "--save", "--confirm-overwrite"]
            for ext in filetypes:
                args += ["--file-filter", "%s|%s" % ext]
            args += ["--title", title]
            file = check_output(args).decode("utf-8").strip()
            if file:
                filename, ext = os.path.splitext(file)
                if not ext:
                    ext = defaultextension
                return filename + ext
            else:
                return ""
        except CalledProcessError:
            return ""
        except Exception:
            return filedialog.asksaveasfilename(title=title,
                                            defaultextension=defaultextension,
                                            initialdir=initialdir,
                                            filetypes=filetypes,
                                            initialfile=initialfile,
                                            **options)
    else:
        return filedialog.asksaveasfilename(title=title,
                                            defaultextension=defaultextension,
                                            initialdir=initialdir,
                                            filetypes=filetypes,
                                            initialfile=initialfile,
                                            **options)

def askcolor(color=None, **options):
    """ plateform specific color chooser
        return the chose color in #rrggbb format """
    if ZENITY:
        try:
            args = ["zenity", "--color-selection", "--show-palette"]
            if "title" in options:
                args += ["--title", options["title"]]
            if color:
                args += ["--color", color]
            color = check_output(args).decode("utf-8").strip()
            if color:
                if color[0] == "#":
                    if len(color) == 13:
                        color = "#%s%s%s"  % (color[1:3], color[5:7], color[9:11])
                elif color[:3] == "rgb":
                    color = color[4:-1].split(",")
                    color = '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))
                else:
                    raise TypeError("Color formatting not understood.")
            return color
        except CalledProcessError:
            return ""
        except Exception:
            color = colorchooser.askcolor(color, **options)
            return color[1]
    else:
        color = colorchooser.askcolor(color, **options)
        return color[1]

def valide_entree_nb(d, S):
    """ commande de validation des champs devant contenir
        seulement des chiffres """
    if d == '1':
        return S.isdigit()
    else:
        return True
