#! /usr/bin/env python3
#
# This script creates some images allowing to test most features of this
#   package

import os
import sys

import smilPython as sp
import smilPyQtGui as sg


# =============================================================================
#
#
def initImages():
  def mkImage(im):
    w = im.getWidth()
    h = im.getHeight()
    m = min(h, w)
    v = im.getDataTypeMax()
    #print(m, v)
    for i in range(0, m):
      im.setPixel(i, i, v)
      im.setPixel(m - 1 - i, i, v)
      im.setPixel(i, m // 2, v)
      im.setPixel(i, m // 2 + 1, v)
      im.setPixel(m // 2, i, v)
      im.setPixel(m // 2 + 1, i, v)

  def mk3DImage(im):
    xmax = im.getWidth() // 2
    depth = im.getDepth()
    for z in range(0, depth):
      #print("z {:3d}".format(z))
      f = z % 64
      if z >= 64:
        f = 64 - f
      for i in range(f, xmax - f):
        im.setPixel(i + f, f + xmax - 1 - i, z, 255)
        im.setPixel(xmax + i - f, i + f, z, 255)
        im.setPixel(i + f, xmax + i - f, z, 255)
        im.setPixel(xmax + i - f, 255 - i - f, z, 255)
    sp.dilate(im, im)

  images = []

  im = sp.Image()
  mkImage(im)
  im.setName("im 256x256")
  images.append(im)

  if True:
    im = sp.Image(512, 256)
    mkImage(im)
    im.setName("im 512x256")
    images.append(im)

  if True:
    im = sp.Image()
    for i in range(0, im.getWidth()):
      for j in range(0, im.getHeight()):
        im.setPixel(i, j, (i + j) // 2 % 256)
    im.setName("im gradient")
    images.append(im)

  if True:
    im = sp.Image(256, 256, 1, 'UINT16')
    mkImage(im)
    im.setName("im 256x256 UINT16")
    images.append(im)

  if True:
    im = sp.Image()
    w = im.getWidth()
    h = im.getHeight()
    hc = h // 2
    for i in range(0, w):
      for j in range(hc - 8, hc + 8):
        im.setPixel(i, j, 255)
    im.setName("im 256x256 HBAR")
    images.append(im)

  if True:
    im = sp.Image(256, 256, 128)
    mk3DImage(im)
    sp.dilate(im, im)
    im.setName("im 3D 256x256x64")
    images.append(im)

    im2 = sp.Image(im)
    sp.dilate(im, im2, sp.Cross3DSE(2))
    im2.setName("im 3D half")
    sp.div(im2, 2, im2)
    images.append(im2)

  files = [
    "images/astronaut-bw.png", "images/distances.png", "images/eutectic.png",
    "images/eutectic-label.png"
  ]
  for fim in files:
    if not os.path.isfile(fim):
      continue
    im = sp.Image(fim)
    #sp.scale(im, 0.5, im)
    im.setName(fim)
    images.append(im)

  return images

# =============================================================================
#
#
def main(cli, args=None):

  images = initImages()

  gui = sg.smilGui()

  views = []
  for im in images:
    gui.imView(im)

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

  #gSmilGui.viewManager()

  r = input("Hit any key to quit")


# =============================================================================
#
#
if __name__ == '__main__':
  sys.exit(main(sys.argv))
