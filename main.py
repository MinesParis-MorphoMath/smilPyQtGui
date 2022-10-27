#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  smilMainWindow.py
#
#  Copyright 2022 José Marcio Martins da Cruz <martins@jose-marcio.org>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#

#
# This script does...
#
# History : xx/xx/xxxx - Jose-Marcio Martins da Cruz
#           Just created
#

import os
import sys
import inspect

import uuid

#import glob
#import psutil

#import fnmatch as fn
import re
import datetime
import time

import argparse as ap
import configparser as cp

import math as m
import numpy as np

import smilPython as sp

from smilPyQtGui import *

import smilPyQtTools as spqt


# -----------------------------------------------------------------------------
#
#
def appLoadConfigFile(fconfig=None):
  if fconfig is None:
    return None

  if not os.path.isfile(fconfig):
    return None

  config = cp.ConfigParser(interpolation=cp.ExtendedInterpolation(),
                           default_section="default")

  config.BOOLEAN_STATES['Vrai'] = True
  config.BOOLEAN_STATES['Faux'] = False

  config.read(fconfig)

  return config


# -----------------------------------------------------------------------------
#
#
def appShowConfigFile(config=None):
  if config is None:
    return
  sections = config.sections()
  for ks in sections:
    print("[{:s}]".format(ks))
    s = config[ks]
    for k in s.keys():
      print("  {:20s} : {:s}".format(k, s[k]))

    print()


# -----------------------------------------------------------------------------
#
#
debug = False
verbose = False


def getCliArgs():
  parser = ap.ArgumentParser()

  parser.add_argument('--debug', help='', action="store_true")
  parser.add_argument('--verbose', help='', action="store_true")

  parser.add_argument('--showconf', help='', action="store_true")
  parser.add_argument('--showargs', help='', action="store_true")

  parser.add_argument('--int', default=None, help='PID to monitor', type=int)
  parser.add_argument('--str', default="String", help='A string', type=str)

  cli = parser.parse_args()

  global debug, verbose

  debug = cli.debug
  verbose = cli.verbose

  return cli


# =============================================================================
#
#
def main(cli, config, args=None):
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

  app = QApplication(sys.argv)

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

  files = ["images/astronaut-bw.png", "images/astronaut-small.png"]
  files = ["images/astronaut-bw.png", "images/distances.png"]
  for fim in files:
    if not os.path.isfile(fim):
      continue
    im = sp.Image(fim)
    #sp.scale(im, 0.5, im)
    im.setName(fim)
    images.append(im)

  windows = []
  for im in images:
    w = smilQtGui(im)
    windows.append(w)

  print()

  spqt.SRegister.print()

  #spqt.SRegister.hideAll()
  #time.sleep(10)
  #spqt.SRegister.showAll()

  if True:
    r = input("Type any key to quit")
    return r
  else:
    return app.exec_()


# =============================================================================
#
#
if __name__ == '__main__':
  os.environ['QT_LOGGING_RULES'] = "*.debug=false"

  cli = getCliArgs()

  bAppl = os.path.basename(sys.argv[0])
  bConf = bAppl.replace('.py', '.conf')
  fConfig = os.path.join('etc', bConf)
  config = None
  if os.path.isfile(fConfig):
    config = appLoadConfigFile(fConfig)

  if cli.showconf:
    appShowConfigFile(config)
  if cli.showargs:
    showArgs(cli, True)
  if cli.showconf or cli.showargs:
    sys.exit(0)

  sys.exit(main(cli, config, sys.argv))
