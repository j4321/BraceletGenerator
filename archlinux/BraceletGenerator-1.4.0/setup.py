#! /usr/bin/python3
# -*- coding:Utf-8 -*-


from setuptools import setup
import os

doc = [os.path.join("doc", f) for f in os.listdir("doc")] 
doc.extend(["CHANGELOG", "README"])
images = [os.path.join("images", f) for f in os.listdir("images")]
examples = [os.path.join("examples", f) for f in os.listdir("examples")]

setup(name = "bracelet-generator",
      version = "1.4.0",
      description = "A friendship bracelet pattern designer",
      author = "Juliette Monsel",
      author_email = "j_4321@sfr.fr",
      url = "https://braceletgenerator.sourceforge.io/index.html",
      license = "GNU General Public License v3",
      packages = ['BraceletGenerator'],
      scripts = ["bracelet-generator"],
      data_files=[("share/locale/en_US/LC_MESSAGES/", ["locale/en_US/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("share/locale/fr_FR/LC_MESSAGES/", ["locale/fr_FR/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("share/doc/bracelet-generator", doc),
                  ("share/bracelet-generator/images", images),
                  ("share/bracelet-generator/examples", examples)],
      long_description = """Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, change the colors.
With the two-colored motif editor, create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpeg, .ps and in text format.""",
      requires = ["PIL","tkinter","sys","os","pickle","locale","gettext"]
)





