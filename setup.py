#! /usr/bin/python3
# -*- coding:Utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from sys import platform

files = ["images/*", "doc/*", "locale/en_US/LC_MESSAGES/*", "locale/fr_FR/LC_MESSAGES/*"]

if platform == 'linux':
    # icon and .desktop file
    data_files = [("share/pixmaps", ["bracelet-generator.svg"]),
                  ("share/applications", ["bracelet-generator.desktop"])]
else:
    data_files = []
    
setup(name = "BraceletGenerator",
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





