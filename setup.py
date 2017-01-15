#! /usr/bin/python3
# -*- coding:Utf-8 -*-

from setuptools import setup
from sys import platform
import os

if platform == 'linux':
    files = []
    doc = ["BraceletGenerator/doc/doc_install_linux.html",
           "BraceletGenerator/doc/doc_fr_install_linux.html",
           "BraceletGenerator/doc/style.css"]
    doc.extend(["README.rst"])
    images = [os.path.join("BraceletGenerator", "images", f) for f in os.listdir("BraceletGenerator/images")]
    examples = [os.path.join("examples", f) for f in os.listdir("examples")]
    data_files = [("share/pixmaps", ["bracelet-generator.svg"]),
                  ("share/locale/en_US/LC_MESSAGES/", ["BraceletGenerator/locale/en_US/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("share/locale/fr_FR/LC_MESSAGES/", ["BraceletGenerator/locale/fr_FR/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("share/doc/bracelet-generator", doc),
                  ("share/man/man1", ["bracelet-generator.1.gz"]),
                  ("share/bracelet-generator/images", images),
                  ("share/doc/bracelet-generator/images", images),
                  ("share/bracelet-generator/examples", examples),
                  ("share/applications", ["bracelet-generator.desktop"])]
else:
    files = ["images/*", "doc/doc.html", "doc/doc_fr.html", "doc/style.css", "locale/en_US/LC_MESSAGES/*", "locale/fr_FR/LC_MESSAGES/*"]
    data_files = []
    
setup(name = "bracelet-generator",
      version = "1.4.0",
      description = "Friendship bracelet pattern designer",
      author = "Juliette Monsel",
      author_email = "j_4321@protonmail.com",
      url = "https://braceletgenerator.sourceforge.io/",
      license = "GNU General Public License v3",
      packages = ['BraceletGenerator'],
      package_data = {'BraceletGenerator' : files},
      data_files = data_files,
      scripts = ["bracelet-generator"],
      long_description = """Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, change the colors.
With the two-colored motif editor, create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpe, .ps and in text format.""",
      requires = ["PIL","tkinter","sys","os","pickle","locale","gettext"]
)





