
# smilPyQtGui

This package provides a graphical user interface to be used with the
[Smil](https://smil.cmm.minesparis.psl.eu) (Simple Morphological Image Library).

*Smil* library has, integrated into it, some code allowing the visualisation of images being handled by the library. This code is based on the *Qt* library. This part of code has been a problem as some Linux distributions comes with recent versions of *Qt*, while others come with very old versions. At the same time, *Smil* developpers must be able to maintain the code compatibility with a large range of versions while following new versions of *Qt*. This is sometimes harder than maintaining the real goal of the library.

This package has almost the same features of the integrated visualisation features, but all this is pushed to the *Python* *PyQt* libraries. With the advantage of being easier to add new features without touching the C++ code of the *Smil* library.

The current default behaviour of *Smil* compile time configuration is to enable the search for *Qt* libraries. In a near future this will be disabled and no more included in packaged distributions of *Smil*

## Example code using smilPyQtGui

This is a minimal
```Python

import sys
import smilPython as sp
import smilPyQtGui as sg

# Initialize the GUI
gui = sg.smilGui()

# Open an image file and create a view for it
fin = "images/astronaut-bw.png"
im1 = sp.Image(fin)
gui.imView(im1)

# Create an eroded image and create a view for it
im2 = sp.Image(im1)
sp.erode(im1, im2)
gui.imView(im2)

r = input("Hit any key to exit")

sys.exit(0)
```
## Installing smilPyQtGui

For the moment, the package hasn't a standard installation script but it's quite easy to install it.

First of all you must be sure you had installed all required packages :

```
smilPython
python3-pyqt5      # package name under Ubuntu and Debian
python3-pyqt5.qwt  # package name under Ubuntu and Debian
```
Download ```smilPyQtGui``` by cloning it somewhere in you computer :

```bash
git clone https://github.com/MinesParis-MorphoMath/smilPyQtGui.git
```

You must decide where to install it :

  - system wide : ```DEST=/usr/local/lib/python3.X/site-packages```
  - user space : ```DEST=~/.local/lib/python3.8/site-packages```

And just do :

```bash
mkdir -p $DEST
cd smilPyQtGui/src
rsync -av --delete smilPyQtGui $DEST/
```

## Available functions in the Python interface


  - ```imView(img = None)``` :   
    Create a view for the Smil image ```img```
  - ```imSetVisible(img = None, visible=True)``` :   
    show/hide the view attached to the image ```img```, depending on the value of ```visible``` parameter
  - ```imSetVisibleAll(visible=True)``` :   
    the same as above but for all views
  - ```imHide(img = None)``` :  
    The same as ```imSetVisible(img, False)``` 
  - ```imHideAll()```  
    The same as ```imSetVisibleAll(False)``` 
  - ```imShow(img = None)```  
    The same as ```imSetVisible(img, True)``` 
  - ```imShowAll()```  
    The same as ```imSetVisibleAll(True)``` 
  - ```imClose(img = None)``` :  
    Close the view of image ```img``` 
  - ```imCloseAll()``` :  
    Close all views 
  - ```viewManager()```  
    Open an window allowing to manage the views : show/hide/close
  - ```listViews()```:  
    Print on the terminal the list of views 




