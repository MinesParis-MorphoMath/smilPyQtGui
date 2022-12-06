
# smilPyQtGui


```Python
import smilPython as sp
import smilPyQtGui as sg


images = initImages()

gui = sg.smilGui()

views = []
for im in images:
  gui.imShow(im)

r = input("Hit any key to continue")

gui.imHide(images[2])

r = input('Hit any key')

gui.imHide('9')
gui.viewManager()

gui.imClose('4')
gui.viewManager()

gui.listViews()

r = input('Hit any key to quit')
return 0
```
