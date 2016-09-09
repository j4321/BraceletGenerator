#! /usr/bin/python3
# -*- coding:Utf-8 -*-

from distutils.core import setup
import os
import sys

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.

files = ["images/*", "doc/*", "locale/en_US/LC_MESSAGES/*", "locale/fr_FR/LC_MESSAGES/*"]

if sys.argv[1] == "install":
    os.system("sudo python2 preinst.py")

setup(name = "BraceletGenerator",
      version = "1.3.2",
      description = "A friendship bracelet pattern designer",
      author = "Juliette Monsel",
      author_email = "j_4321@sfr.fr",
      url = "http://braceletgenerator.sourceforge.net/index.html",
      license = "GNU General Public License v3",
      #Name the folder where your packages live:
      #(If you have other packages (dirs) or modules (py files) then
      #put them into the package directory - they will be found
      #recursively.)
      packages = ['BraceletGenerator'],
      #'package' package must contain files (see list above)
      #I called the package 'package' thus cleverly confusing the whole issue...
      #This dict maps the package name =to=> directories
      #It says, package *needs* these files.
      package_data = {'BraceletGenerator' : files },
      #'runner' is in the root.
      scripts = ["bracelet-generator"],
      long_description = """Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, change the colors.
With the two-colored motif editor, create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpeg and .ps.""",
      requires = ["PIL","tkinter","sys","os","tkinter.ttk","pickle","locale","gettext"]
)





