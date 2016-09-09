Bracelet Generator - An easy way to design friendship bracelet patterns
Copyright 2014-2016 Juliette Monsel <j_4321@sfr.fr>


This software doesn’t aim at teaching you how to make friendship bracelets.
It only enables you to create patterns easily. So if you don’t know how to
make the four types of knots, find a tutorial on the Internet first,
for instance http://friendship-bracelets.net/tutorials.php.

----------------Download---------------------------------------------------

* Windows: bracelet-generator-version.exe.

* Ubuntu/Debian (it might work for other Debian based distributions, 
  but I have not tested all of them): bracelet-generator-version_all.deb.
   
* OS X (tested on El Capitan): bracelet-generator-version-osx.zip

* Archlinux: bracelet-generator is available on AUR 
  https://aur.archlinux.org/packages/bracelet-generator
   
* Others: bracelet-generator-version-src.tar.xz

Since python is an interpreted language the source code does not need to 
be compiled, and is not difficult to use.

-----------------Install---------------------------------------------------
1. Windows

Launch bracelet-generator-version.exe and follow the instructions.

2. Ubuntu/Debian

First, you need to install a few dependencies if they are missing: 
python3-pil, python3-tk, ghostscript, zenity.

You can use "dpkg-query -W <package>" in the console to check whether 
<package> is installed.

Then, open a console and run
$ sudo dpkg -i bracelet-generator-version_all.deb

3. OS X

Unzip the archive. Then launch BraceletGenerator.app 
(you can move it first to /Applications). 
I apologize for the poor quality of the images/icons, but python 
for OS X does not support Tcl/Tk 8.6, so I have to make do with the
limitations of the 8.5 version.

4. Source code

First, you need to install a few dependencies if they are missing: 
- Python 3 (I used the 3.5 version but it might work as well with 
  older version) https://www.python.org/downloads/release/python-352/
  
- Tkinter (TCL/Tk GUI for Python)

- Pillow (Python Imaging Library) 
  https://pypi.python.org/pypi/Pillow/3.3.1
  
- Ghostscript (to be able to export the pattern in .png or .jpg) 
  http://ghostscript.com/download/gsdnld.html
  
- For linux distributions: zenity (to have a better integration of the 
  file browser in the theme), in Windows and OS X, Tkinter file browser 
  is well integrated.

Usually Python 3 is already installed in linux but you need to install 
Tkinter. On the contrary, in Windows, you need to install Python 3 and 
it installs Tkinter at the same time.

For linux/unix distributions, the names of the packages vary. 
Here are the name for:
- Ubuntu : python3-pil, python3-tk, ghostscript, zenity
- Archlinux : python-pillow, tk, ghostscript, zenity
Otherwise, you can install the pillow using pip:
$ sudo pip3 install pillow 

Otherwise, see the documentation for more information.

Unzip the archive and launch bracelet-generator.py: either make it 
executable or run it with python.
$ python3 bracelet-generator.py

You can also install BraceletGenerator with (need administrator / 
superuser rights)
$ python3 setup.py install 
Then, at least in linux, it can be launched from the console with
$ bracelet-generator

---------------------------------------------------------------------------

If you have any trouble/comment/question, write me an email at 
j_4321@sfr.fr.



