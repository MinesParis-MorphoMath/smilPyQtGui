
import os
import sys

import smilPython as sp

from smilPyQtView import *

# =============================================================================
#
#
def main(args=None):
  fin = "images/astronaut-bw.png"
  im1 = sp.Image(fin)
  smilQtView(im1)
  im2 = sp.Image(im1)
  sp.erode(im1, im2)
  smilQtView(im2)

  r = input("Hit any key to quit")

# =============================================================================
#
#
if __name__ == '__main__':
  sys.exit(main(sys.argv))
