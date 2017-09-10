Bracelet Generator
==================

Bracelet Generator is a friendship bracelet pattern designer.
It enables you to easily design your own patterns, add rows and strings, 
change the colors. With the two-colored motif editor, 
create your motif and the pattern will automatically be generated.
The patterns can be exported in .png, .jpeg, .ps and in text format.

This software doesn’t aim at teaching you how to make friendship bracelets.
It only enables you to create patterns easily. So if you don’t know how to
make the four types of knots, find a tutorial on the Internet first,
for instance `friendship-bracelet.net <http://friendship-bracelets.net/tutorials.php>`__.


Install
=======

Since python is an interpreted language the source code does not need to 
be compiled, and is not difficult to use.

The downloaded package can be checked using the checksums provided by the `sha512sums.txt` file.

Windows
-------

Download and launch bracelet-generator-x.y.z.exe and follow the instructions.

Ubuntu
------

Bracelet Generator is available in the PPA `ppa:j-4321-i/ppa`.
    
    ::
        
        $ sudo add-apt-repository ppa:j-4321-i/ppa
        $ sudo apt-get update
        $ sudo apt-get install bracelet-generator

Archlinux
---------

Bracelet Generator is available in `AUR <https://aur.archlinux.org/packages/bracelet-generator>`__.

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

If you encounter bugs or if you have suggestions, please open an issue 
on `GitHub <https://github.com/j4321/BraceletGenerator/issues>`__ or write me an 
email at <j_4321@protonmail.com>.
