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


IM_QUESTION_DATA and IM_WARNING_DATA was taken from "tk8.6/icons.tcl":

    A set of stock icons for use in Tk dialogs. The icons used here
    were provided by the Tango Desktop project which provides a
    unified set of high quality icons licensed under the
    Creative Commons Attribution Share-Alike license
    (http://creativecommons.org/licenses/by-sa/3.0/)

    See http://tango.freedesktop.org/Tango_Desktop_Project

    Copyright (c) 2009 Pat Thoyts <patthoyts@users.sourceforge.net>

Most of the other icons are modified versions of icons from the elementary project
Copyright 2007-2013 elementary LLC, except a few I designed myself.


Constants and global functions of Bracelet Generator
"""


from locale import getdefaultlocale
import os
from tkinter import TclVersion
from sys import platform
import gettext
from configparser import ConfigParser
from webbrowser import open as webOpen
from subprocess import check_output, CalledProcessError
from colorsys import hsv_to_rgb, rgb_to_hsv
from tkinter import filedialog
from tkinter import colorchooser

PL = os.name
STYLE = 'clam'

# ---  paths
PATH = os.path.split(__file__)[0]
if platform == 'linux' and (not os.access(PATH, os.W_OK) or not os.path.exists(os.path.join(PATH, "images"))):
    IMAGES_LOCATION = '/usr/share/bracelet-generator/images'
    PATH_LOCALE = "/usr/share/locale"
    DOC = '/usr/share/doc/bracelet-generator/doc_install_linux.html'
    DOC_FR = '/usr/share/doc/bracelet-generator/doc_fr_install_linux.html'
else:
    IMAGES_LOCATION = os.path.join(PATH, 'images')
    PATH_LOCALE = os.path.join(PATH, "locale")
    DOC = os.path.join(PATH, "doc", "doc.html")
    DOC_FR = os.path.join(PATH, "doc", "doc_fr.html")

LOCAL_PATH = os.path.join(os.path.expanduser("~"), "BraceletGenerator")
if not os.path.exists(LOCAL_PATH):
    os.mkdir(LOCAL_PATH)
# temporary file
TMP_PS = os.path.join(LOCAL_PATH, ".tmp.ps")
# config file
PATH_CONFIG = os.path.join(LOCAL_PATH, 'BraceletGenerator.ini')
# bracelet log file
BRACELET_LOG = os.path.join(LOCAL_PATH, "BraceletGenerator%i.log")
i = 0
while os.path.exists(BRACELET_LOG % (i)):
    i += 1
BRACELET_LOG %= i
# bicolore log file
BICOLOR_LOG = os.path.join(LOCAL_PATH, "Bicolor%i.log")
i = 0
while os.path.exists(BICOLOR_LOG % (i)):
    i += 1
BICOLOR_LOG %= i

# ---  configuration file
CONFIG = ConfigParser()
if os.path.exists(PATH_CONFIG):
    CONFIG.read(PATH_CONFIG)
    LANGUE = CONFIG.get("General", "language")
    if not CONFIG.has_option("General", "check_update"):
        CONFIG.set("General", "check_update", "True")
else:
    LANGUE = ""

    CONFIG.add_section("General")
    CONFIG.set("General", "last_path", LOCAL_PATH)
    CONFIG.set("General", "recent_files", "")
    CONFIG.set("General", "recent_bicolor", "")
    CONFIG.set("General", "language", "en")
    CONFIG.set("General", "check_update", "True")

    CONFIG.add_section("Bracelet")
    CONFIG.set("Bracelet", "row_nb", "4")
    CONFIG.set("Bracelet", "string_nb", "4")
    CONFIG.set("Bracelet", "default_color", "#ff0000")


def save_config():
    """ sauvegarde du dictionnaire contenant la configuration du logiciel (langue ...) """
    CONFIG.set("General", "recent_files", ",".join(RECENT_FILES))
    CONFIG.set("General", "recent_bicolor", ",".join(RECENT_BICOLOR))
    with open(PATH_CONFIG, 'w') as fichier:
        CONFIG.write(fichier)


# ---  Translation
APP_NAME = "BraceletGenerator"

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
try:
    gettext.bind_textdomain_codeset(APP_NAME, 'UTF-8')
except AttributeError:
    pass
gettext.bindtextdomain(APP_NAME, PATH_LOCALE)
gettext.textdomain(APP_NAME)
LANG = gettext.translation(APP_NAME, PATH_LOCALE,
                           languages=[LANGUE], fallback=True)
LANG.install()

# ---  get recent files
RECENT_FILES = CONFIG.get("General", "recent_files").split(",")
if RECENT_FILES == [""]:
    RECENT_FILES = []
RECENT_BICOLOR = CONFIG.get("General", "recent_bicolor").split(",")
if RECENT_BICOLOR == [""]:
    RECENT_BICOLOR = []

# ---  pictures
IM_EXIT_M = os.path.join(IMAGES_LOCATION, "exit_m.png")
IM_EXIT = os.path.join(IMAGES_LOCATION, "exit.png")
IM_EXPORT_M = os.path.join(IMAGES_LOCATION, "export_m.png")
IM_EXPORT = os.path.join(IMAGES_LOCATION, "export.png")
IM_EXPORT_TXT_M = os.path.join(IMAGES_LOCATION, "export_txt_m.png")
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

IM_QUESTION_DATA = """
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
SUVORK5CYII=
"""

IM_WARNING_DATA = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAABSZJREFU
WIXll1toVEcYgL+Zc87u2Yu7MYmrWRuTJuvdiMuqiJd4yYKXgMQKVkSjFR80kFIVJfWCWlvpg4h9
8sXGWGof8iKNICYSo6JgkCBEJRG8ImYThNrNxmaTeM7pQ5IlJkabi0/9YZhhZv7///4z/8zPgf+7
KCNRLgdlJijXwRyuDTlcxV9hbzv8nQmxMjg+XDtiOEplkG9PSfkztGmTgmFQd+FCVzwa3fYN/PHZ
AcpBaReicW5xcbb64IEQqko8Lc26d/58cxS+/BY6hmJvyEfQBoUpwWCmW1FErKaGWHU13uRk4QkE
UtxQNFR7QwIoB4eiKD9PWbVKbb10CZmaCqmpxCormRYO26QQx85B0mcD+AeK0xYvHqu1tNDx+DH6
gQM4jh0j3tCA3tGBLyfHLuD7zwJwAcYqun44sHy51nr5MsqsWWj5+djCYdS5c4ldvUr24sU2qarf
lUL6qAN0wqH0vDy7+fAhXZEI+v79CNmt7igpofPVK5SmJvyhkJBwYlQBSiHd7vUWZ86bp8WqqtCW
LkVbuBAhBEIItGAQ2+rVxG7cICMY1KTDsekc5IwagIQTmStXis47dzBiMfR9+xCi+wb39s79+zFi
MczGRjLmzTMlnBoVgLMwyzF+/Cb/lClq2/Xr2AoKUKdPxzAMWltbiUajmKaJkpGBY8sW3tbW4g8E
VNXrXVEKK0YMoMKp7Px8K15Tg2VZOHbvBiASiRAMBgkGg0QiEYQQOIuLsRSFrnv3yJo/HxVOW594
7D4KUAa57qysvNSUFOVtbS32rVuRfj9CCFwuV2Kfy+VCCIFMScFVVET7/fukJidLm883rQy+HhaA
BUII8cvUNWt4W1WFcLvRd+5MnHl/AOjOB+eOHchx44jX1ZEdCqkSTpaDbcgA5+GrpNmzc9ymKdvr
67Hv2oVMSko4cjgcKIqCoijoup64EdLpxLV3Lx1PnuCVUrgmTfK9hV1DAjgKqlSUk1PCYdl25QrS
70cvLEw4SWS+04nT6XxvXgiBc8MGtKlTaa+rIysnR1Ok/OF38PxngAzY4VuwYKL99WvR8fQpjj17
kLqeiL6393g8eDyeAWBSVfEcOkRXczOOaBRvVpZuDPJEDwD4DVyKrv+UlZurxSorUWfMQC8oGOBc
CDHgC/Rdc4TD2BctIl5fT+bkyTahaXvOw8RPApiwd2Ju7hjZ2EhXSwvOkhKQcoADgIqKCioqKgYc
QW9LOnIEIxZDbWpiXCCABT9+FKAUxtm83pKMUEiLVVejLVqEtmTJB50LIdi2bRuFPbnRd7232efM
wbVuHR2PHjHR77dJXS8sg5mDAihweFJenmrevYvR1oazpGTQ6IQQaJqG7ClI/dd655IOHsSyLMSL
F6QFAib9nugEQClk2Xy+orTsbK3t1i3sa9ei5eQMGr0QgvLyci5evDiocyEEtsxMPNu30/nsGRO8
XlVzu8NlkNvrV+0T/fHMZcusrtu3MeNx9PXrobUVq8cYQrw3TrRub1h9+v573Bs3Ej1zBvP5c/zp
6dbLhoaTwPy+ANKCfF92thq7dg2A6JYt/fNlxGK8eUNSerryHEJHQT8K8V4A5ztojty8OeaLzZul
1DSwLCzDANPEMozusWFgmWZ33288YK3/nGlixuM0v3xpWfDX0Z4i1VupXEWwIgRnJfhGPfQ+YsLr
+7DzNFwCuvqWyiRg7DSYoIBu9smPkYqEd4AwIN4ITUAL0A4Da7UC6ICdEfy2fUBMoAvo7GnWKNoe
mfwLcAuinuFNL7QAAAAASUVORK5CYII=
"""

# ---  colors
if platform == 'darwin' or PL == 'nt':
    BG_COLOR = '#F0F0F0'
    CANVAS_COLOR = "#ffffff"
else:
    BG_COLOR = '#cecece'
    CANVAS_COLOR = '#E8E8E8'


def hsv_to_html(h, s, v):
    r, g, b = hsv_to_rgb(h / 360, s / 100, v / 100)
    r, g, b = round(r * 255), round(g * 255), round(b * 255)
    return ("#%2.2x%2.2x%2.2x" % (r, g, b)).upper()


def html_to_hsv(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:], 16)
    h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
    return round(h * 360), round(s * 100), round(v * 100)


def rgb_to_html(r, g, b):
    return ("#%2.2x%2.2x%2.2x" % (r, g, b)).upper()


def html_to_rgb(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:], 16)
    return r, g, b


def active_color(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:], 16)
    r += (255 - r) / 3
    g += (255 - g) / 3
    b += (255 - b) / 3
    return ("#%2.2x%2.2x%2.2x" % (round(r), round(g), round(b))).upper()


def fill(image, color):
    """Fill image with a color=#hex."""
    width = image.width()
    height = image.height()
    horizontal_line = "{" + " ".join([color] * width) + "}"
    image.put(" ".join([horizontal_line] * height))


# ---  platform dependent mouse events
if PL == "nt":

    def mouse_wheel(event):
        """ gestion de la molette de la souris sous windows """
        return -1 * (event.delta // 120)

    MOUSEWHEEL = ["<MouseWheel>"]
    RIGHT_CLICK = '<Button-3>'
elif platform == "darwin":

    def mouse_wheel(event):
        """ gestion de la molette de la souris """
        return -1 * (event.delta)

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


# ---  display help


def help(event=None):
    """ ouvre l'aide en .html dans la langue de l'interface """
    if LANGUE[:2] == "fr":
        webOpen(DOC_FR)
    else:
        webOpen(DOC)


def help_web(event=None):
    """ ouvre l'aide en ligne dans la langue de l'interface """
    if LANGUE[:2] == "fr":
        webOpen("https://braceletgenerator.sourceforge.io/index_fr.html")
    else:
        webOpen("https://braceletgenerator.sourceforge.io/")


# ---  compatibility with tcl8.5
if TclVersion < 8.6:
    # then tkinter cannot import PNG files directly, we need to use PIL
    from PIL import Image, ImageTk
    from BraceletGenerator.custom_messagebox import ob_checkbutton
    if not CONFIG.has_option("General", "old_tcl_warning") or CONFIG.getboolean("General", "old_tcl_warning"):
        ans = ob_checkbutton(title=_("Information"), image=IM_WARNING_DATA,
                             message=_("This software has been developped using Tcl/Tk 8.6, but you are using an older version. Please consider upgrading your Tcl/Tk version."),
                             checkmessage=_("Do not show this message again."),
                             className="BraceletGenerator")
        CONFIG.set("General", "old_tcl_warning", str(not ans))

    def open_image(file, master=None):
        return ImageTk.PhotoImage(Image.open(file), master=master)

else:
    # no need of ImageTk dependency
    from tkinter import PhotoImage

    def open_image(file, master=None):
        return PhotoImage(file=file, master=master)


# ---  icon
def set_icon(fen):
    """ icône de l'application """
    if PL == 'nt':
        fen.iconbitmap(IM_ICON_WIN, default=IM_ICON_WIN)
    else:
        icon = open_image(file=IM_ICON16, master=fen)
        fen.iconphoto(True, icon)


# ---  filebrowser
ZENITY = False

try:
    import tkfilebrowser as tkfb
except ImportError:
    tkfb = False

try:
    import tkcolorpicker as tkcp
except ImportError:
    tkcp = False

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
    if tkfb:
        return tkfb.askopenfilename(title=title,
                                    defaultext=defaultextension,
                                    filetypes=filetypes,
                                    initialdir=initialdir,
                                    initialfile=initialfile,
                                    **options)
    elif ZENITY:
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
    if tkfb:
        return tkfb.asksaveasfilename(title=title,
                                      defaultext=defaultextension,
                                      initialdir=initialdir,
                                      filetypes=filetypes,
                                      initialfile=initialfile,
                                      **options)
    elif ZENITY:
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
    if tkcp:
        color = tkcp.askcolor(color, **options)
        if color:
            return color[1]
        else:
            return None
    elif ZENITY:
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
                        color = "#%s%s%s" % (color[1:3], color[5:7], color[9:11])
                elif color[:4] == "rgba":
                    color = color[5:-1].split(",")
                    color = '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))
                elif color[:3] == "rgb":
                    color = color[4:-1].split(",")
                    color = '#%02x%02x%02x' % (int(color[0]), int(color[1]), int(color[2]))
                else:
                    raise TypeError("Color formatting not understood.")
            return color
        except CalledProcessError:
            return None
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
