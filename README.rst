Bracelet Generator
==================

Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, 
change the colors. With the two-colored motif editor, 
create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpeg and .ps.

This software doesn’t aim at teaching you how to make friendship bracelets.
It only enables you to create patterns easily. So if you don’t know how to
make the four types of knots, find a tutorial on the Internet first,
for instance `friendship-bracelet.net <http://friendship-bracelets.net/tutorials.php>`__.


Download
========

- Windows: `bracelet-generator-x.y.z.exe`.

- Ubuntu/Debian (it should work for other Debian based distributions, 
  but I have not tested all of them): `bracelet-generator-x.y.z_all.deb`
  
- OS X (tested on El Capitan): `bracelet-generator-x.y.z-osx.zip`

- Archlinux: bracelet-generator is available on `AUR <https://aur.archlinux.org/packages/bracelet-generator>`__.
   
- Others: `bracelet-generator-x.y.z-src.tar.xz`

Since python is an interpreted language the source code does not need to 
be compiled, and is not difficult to use.

The downloaded package can be checked using the checksums provided by the `sha512sums.txt` file.


Install
=======

Windows
-------

Launch bracelet-generator-x.y.z.exe and follow the instructions.

Ubuntu/Debian
-------------

First, you need to install a few dependencies if they are missing: 
python3-pil, python3-tk, ghostscript, zenity.

You can use `dpkg-query -W <package>` in the console to check whether 
`<package>` is installed.

Then, open a console and run

::

    $ sudo dpkg -i bracelet-generator-x.y.z_all.deb

OS X
----

Unzip the archive. Move BraceletGenerator.app to the /Applications. 
To be able to export patterns in .png or .jpg, 
you need to install Ghostscript. It can be done with brew:

::

    $ brew install ghostscript

Otherwise refer to `Ghostscript website <http://ghostscript.com/>`__. 


Source code
-----------

First, you need to install a few dependencies if they are missing: 

- `Python 3 <https://www.python.org/downloads/release/python-352>`__ (I used the 3.5 version but it might work as well with older version)
  
- Tkinter (TCL/Tk GUI for Python)

- `Pillow <https://pypi.python.org/pypi/Pillow/3.3.1>`__ (Python Imaging Library) 
  
  
- `Ghostscript <http://ghostscript.com/download/gsdnld.html>`__ (to be able to export the pattern in .png or .jpg) 
  
- For linux distributions: zenity (to have a better integration of the file browser in the theme), in Windows and OS X, Tkinter file browser is well integrated.

Usually Python 3 is already installed in linux but you need to install 
Tkinter. On the contrary, in Windows, you need to install Python 3 and 
it installs Tkinter at the same time.

For linux/unix distributions, the names of the packages vary. 
Here are the name for:
- Ubuntu : python3-pil, python3-tk, ghostscript, zenity
- Archlinux : python-pillow, tk, ghostscript, zenity
Otherwise, you can install the pillow using pip:

::

    $ sudo pip3 install pillow 

Otherwise, see the documentation for more information.

Unzip the archive and launch bracelet-generator.py: either make it 
executable or run it with python.

::  

    $ python3 bracelet-generator.py

You can also install BraceletGenerator with (need administrator / 
superuser rights)

::

    $ python3 setup.py install 
    
Then, at least in linux, it can be launched from the console with

::

    $ bracelet-generator


---------------------------------------------------------------------------

If you have any trouble/comment/question, write me an email at 
j_4321@protonmail.com.