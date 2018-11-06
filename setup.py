#! /usr/bin/python3
# -*- coding:Utf-8 -*-

from setuptools import setup
from sys import platform
import os

with open("BraceletGenerator/version.py") as file:
    exec(file.read())
    
if 'linux' in platform:
    files = []
    doc = ["BraceletGenerator/doc/doc_install_linux.html",
           "BraceletGenerator/doc/doc_fr_install_linux.html",
           "BraceletGenerator/doc/style.css"]
    doc.extend(["README.rst", "changelog"])
    images = [os.path.join("BraceletGenerator", "images", f) for f in os.listdir("BraceletGenerator/images")]
    examples = [os.path.join("examples", f) for f in os.listdir("examples")]
    data_files = [("/usr/share/pixmaps", ["bracelet-generator.svg"]),
                  ("/usr/share/locale/en_US/LC_MESSAGES/", ["BraceletGenerator/locale/en_US/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("/usr/share/locale/fr_FR/LC_MESSAGES/", ["BraceletGenerator/locale/fr_FR/LC_MESSAGES/BraceletGenerator.mo"]),
                  ("/usr/share/doc/bracelet-generator", doc),
                  ("/usr/share/man/man1", ["bracelet-generator.1.gz"]),
                  ("/usr/share/bracelet-generator/images", images),
                  ("/usr/share/doc/bracelet-generator/images", images),
                  ("/usr/share/bracelet-generator/examples", examples),
                  ("/usr/share/applications", ["bracelet-generator.desktop"])]
else:
    files = ["images/*", "doc/doc.html", "doc/doc_fr.html", "doc/style.css", "locale/en_US/LC_MESSAGES/*", "locale/fr_FR/LC_MESSAGES/*"]
    data_files = []

setup(name="bracelet-generator",
      version=__version__,
      description="Friendship bracelet pattern designer",
      author="Juliette Monsel",
      author_email="j_4321@protonmail.com",
      url="https://j4321.github.io/BraceletGenerator/",
      license="GPLv3",
      packages=['BraceletGenerator'],
      package_data={'BraceletGenerator' : files},
      data_files=data_files,
      scripts=["bracelet-generator"],
      long_description="""Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, change the colors.
With the two-colored motif editor, create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpeg, .ps and in text format.""",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'Topic :: Multimedia :: Graphics',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Natural Language :: English',
          'Natural Language :: French',
          'Operating System :: OS Independent',
      ],
      requires=["Pillow"]
)





