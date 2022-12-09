#! /usr/bin/env python3
#
# This script just reads an image file, create another one from the erosion
#   of the first one and show both

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
