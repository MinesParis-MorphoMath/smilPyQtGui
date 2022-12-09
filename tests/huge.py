#! /usr/bin/env python3
#
# This script creates a huge image and show it

import os
import sys

import smilPython as sp
import smilPyQtGui as sg

# =============================================================================
#
#
def main(cli, args=None):

  # Initialize the GUI
  gui = sg.smilGui()

  sz = 16000

  im = sp.Image(sz, sz)
  gui.imView(im)

  r = input("Hit any key to quit")


# =============================================================================
#
#
if __name__ == '__main__':
  sys.exit(main(cli, sys.argv))
