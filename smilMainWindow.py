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

import uuid

#import glob
#import psutil

#import fnmatch as fn
import re
import datetime

import argparse as ap
import configparser as cp

import math as m
import numpy as np

#import pandas      as pd
#import statistics  as st
#import scipy.stats as sst
#import seaborn     as sb

import smilPython as sp

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QScrollArea, QMessageBox,
                             QMainWindow, QMenu, QAction, qApp, QFileDialog,
                             QStatusBar, QTextEdit, QWidget)
from PyQt5.QtWidgets import QApplication, QVBoxLayout

import globals as g

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
      #print("  {:20s} : {:32s} # {:s}".format(k, s[k], s.get(k)))

    print()


# -----------------------------------------------------------------------------
#
#
def getCliArgs():
  parser = ap.ArgumentParser()

  parser.add_argument('--debug', help='', action="store_true")
  parser.add_argument('--verbose', help='', action="store_true")

  parser.add_argument('--showconf', help='', action="store_true")
  parser.add_argument('--showargs', help='', action="store_true")

  parser.add_argument('--int', default=None, help='PID to monitor', type=int)
  parser.add_argument('--str', default="String", help='A string', type=str)

  cli = parser.parse_args()
  return cli


# =============================================================================
#
#

sp2npTypes = {
  'UINT8': np.uint8,
  'UINT16': np.uint16,
  'UINT32': np.uint32,
}

# =============================================================================
#
#
class smilCanvas(QLabel):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent
    width, height = parent.width(), parent.height()
    width, height = 128, 128

    self.pixmap = QPixmap(width, height)
    self.pixmap.fill(Qt.GlobalColor.white)
    self.setPixmap(self.pixmap)

    self.setMouseTracking(True)

  #
  # I M A G E
  #
  def smilToNumpyImage(self, z=0):
    parent = self.parent
    self.imArray = np.zeros((parent.h, parent.w, parent.d),
                            dtype=sp2npTypes[parent.imType])
    uLim = parent.image.getDataTypeMax()
    lLim = parent.image.getDataTypeMin()
    Max = sp.maxVal(parent.image)
    Min = sp.minVal(parent.image)
    if Max == Min:
      Max = uLim
      Min = lLim

    if parent.autorange:
      coeff = 255. / (Max - Min)
    else:
      coeff = 255. / (uLim - lLim)

    for i in range(0, parent.w):
      for j in range(0, parent.h):
        self.imArray[j, i] = int(coeff * parent.image.getPixel(i, j, z))

    fmt = "Image : {:6s} : w({:d}) h({:d}) d({:d})"
    print(fmt.format(parent.imType, parent.w, parent.h, parent.d))

  #
  def imageUpdate(self):
    parent = self.parent
    self.smilToNumpyImage()

    fmt = "Image : {:6s} : w({:d}) h({:d}) d({:d})"
    print(fmt.format(parent.imType, parent.w, parent.h, parent.d))

    image = QImage(self.imArray, parent.w, parent.h, QImage.Format_Indexed8)
    self.setPixmap(QPixmap.fromImage(image))
    self.resize(parent.w + 20, parent.h + 80)
    self.setMinimumSize(parent.w, parent.h)
    #self.parent.resize()

  #
  #   E V E N T S
  #
  def mouseMoveEvent(self, event):
    mousePos = event.pos()
    if False and (mousePos.x() < 0 or mousePos.x() >= self.parent.w):
      self.parent.lbl1.setText("")
      return
    if False and (mousePos.y() < 0 or mousePos.y() >= self.parent.h):
      self.parent.lbl1.setText("")
      return

    fmt = "Mouse Coordinates: ({}, {})"
    posText = fmt.format(mousePos.x(), mousePos.y())
    self.parent.lbl1.setText(posText)
    #print(posText)


# =============================================================================
#
#
class smilImageView(QMainWindow):
  def __init__(self, img=None):
    super().__init__()

    self.initializeMembers()
    self.initializeUI()

    self.setupImage(img)
    self.resize(self.w + 20, self.h + 80)

  #
  #
  #
  def initializeMembers(self):
    self.uuid = uuid.uuid4()
    self.imName = ''
    self.scale = 1.
    self.showLabel = False
    self.autorange = False

    self.image = None
    self.imType = ''
    self.w = 0
    self.h = 0
    self.d = 0
    self.imName = ''

  #
  #
  #
  def initializeUI(self):
    """Set up the application's GUI."""
    self.setMinimumSize(200, 200)
    #self.resize(self.w, self.h)
    self.setWindowTitle("Smil Image ")

    self.setUpMainWindow("Nouvelle fenetre")
    self.createActions()
    self.createMenu()

    self.show()

  #
  #
  #
  def setUpMainWindow(self, title=None):

    self.lbl1 = QLabel()
    self.lbl1.setText("Label 1")

    self.canvas = smilCanvas(self)

    vbox = QVBoxLayout()
    vbox.addWidget(self.lbl1)
    vbox.addStretch()
    vbox.addWidget(self.canvas)
    vbox.addStretch()

    tout = QWidget()
    tout.setLayout(vbox)
    self.setCentralWidget(tout)

    self.statusBar = QStatusBar()
    self.setStatusBar(self.statusBar)
    self.statusBar.showMessage("")

  #
  # M E N U S
  #
  def createMenu(self):
    """Create the application's menu bar."""
    self.menuBar().setNativeMenuBar(False)

    # Create File menu and add actions
    file_menu = self.menuBar().addMenu("File")
    #file_menu.addAction(self.open_act)
    file_menu.addAction(self.save_act)
    file_menu.addSeparator()
    file_menu.addAction(self.print_act)
    file_menu.addSeparator()
    file_menu.addAction(self.hide_act)
    file_menu.addAction(self.close_act)

    # Create File menu and add actions
    tools_menu = self.menuBar().addMenu("Tools")
    tools_menu.addAction(self.zoomIn_act)
    tools_menu.addAction(self.zoomOut_act)
    tools_menu.addAction(self.zoomReset_act)
    tools_menu.addSeparator()
    tools_menu.addAction(self.label_act)
    tools_menu.addSeparator()
    tools_menu.addAction(self.info_act)

  def createActions(self):
    """Create the application's menu actions."""

    #
    # File menu
    #
    self.save_act = QAction(QIcon("images/save_file.png"),"Save Snapshot")
    self.save_act.setShortcut("Ctrl+S")
    self.save_act.setStatusTip("Save Snapshot")
    #self.save_act.triggered.connect(self.saveImage)

    self.print_act = QAction(QIcon("images/print.png"), "Print")
    self.print_act.setShortcut("Ctrl+P")
    self.print_act.setStatusTip("Print image")
    #self.print_act.triggered.connect(self.printImage)
    self.print_act.setEnabled(False)

    self.hide_act = QAction(QIcon("images/exit.png"), "Hide Window")
    self.hide_act.setShortcut("Ctrl+Q")
    self.hide_act.setStatusTip("Hide Window")
    #self.hide_act.triggered.connect(self.close)

    self.close_act = QAction(QIcon("images/exit.png"), "Close Window")
    self.close_act.setShortcut("Ctrl+Q")
    self.close_act.setStatusTip("Close Window")
    #self.close_act.triggered.connect(self.close)

    #
    # Tools menu
    #
    self.zoomIn_act = QAction("Zoom In")
    self.zoomIn_act.setShortcut("Ctrl++")
    self.zoomIn_act.setStatusTip("Zoom In image")
    #self.quit_act.triggered.connect(self.close)

    self.zoomOut_act = QAction("Zoom Out")
    self.zoomOut_act.setShortcut("Ctrl+-")
    self.zoomOut_act.setStatusTip("Zoom Out image")
    #self.quit_act.triggered.connect(self.close)

    self.zoomReset_act = QAction("Zoom Reset")
    self.zoomReset_act.setShortcut("Ctrl+=")
    self.zoomReset_act.setStatusTip("Reset Zoom to Original")
    #self.quit_act.triggered.connect(self.close)

    self.label_act = QAction("Show labelled image")
    self.label_act.setShortcut("Ctrl+L")
    self.label_act.setStatusTip("Show labelled image")
    #self.quit_act.triggered.connect(self.close)

    self.info_act = QAction("Image information")
    self.info_act.setShortcut("Ctrl+I")
    self.info_act.setStatusTip("Image information")
    #self.info_act.triggered.connect(self.close)

  #
  # I M A G E
  #
  # TODO check this when handling 3D images
  def setupImage(self, img):
    if img is None:
      img = sp.Image()
    self.image = img
    self.imType = self.image.getTypeAsString()
    self.w = self.image.getWidth()
    self.h = self.image.getHeight()
    self.d = self.image.getDepth()
    self.imName = self.image.getName()
    if self.imName is None or self.imName == '':
      self.imName = "No name"

    self.setWindowTitle(self.imName)
    self.imageUpdate()

  #
  def imageUpdate(self):
    self.canvas.imageUpdate()
    return

  #
  # EVENT HANDLERS
  #
  def XmouseMoveEvent(self, event):
    mousePos = event.pos()
    posText = "Mouse Coordinates: ({}, {})".format(mousePos.x(), mousePos.y())
    print(posText)

  def XmousePressEvent(self, event):
      """Handle when mouse is pressed."""
      if event.button() == Qt.MouseButton.LeftButton:
        print('  Left button')
      else:
        print('  Right button')

# =============================================================================
#
#
def registerWindow():
  pass

def unregisterWindow():
  pass

# =============================================================================
#
#
def main(cli, config, args=None):

  def mkImage(im):
    w = im.getWidth()
    h = im.getHeight()
    m = min(h,w)
    v = im.getDataTypeMax()
    #print(m, v)
    for i in range(0, m):
      im.setPixel(i, i, v)
      im.setPixel(m - 1 - i, i, v)
      im.setPixel(i, m // 2, v)
      im.setPixel(i, m // 2 + 1, v)
      im.setPixel(m // 2, i, v)
      im.setPixel(m // 2 + 1, i, v)

  app = QApplication(sys.argv)

  images = []

  im = sp.Image()
  mkImage(im)
  im.setName("im 256x256")
  images.append(im)

  if False:
    im = sp.Image(512,256)
    mkImage(im)
    im.setName("im 512x256")
    images.append(im)

  if True:
    im = sp.Image(256, 256, 1,'UINT16')
    mkImage(im)
    im.setName("im 256x256 UINT16")
    images.append(im)

  files = ["images/astronaut-bw.png", "images/astronaut-small.png"]
  files = ["images/astronaut-bw.png"]
  for fim in files:
    if not os.path.isfile(fim):
      continue
    im = sp.Image(fim)
    sp.scale(im, 0.5, im)
    im.setName(fim)
    images.append(im)

  windows = []
  for im in images:
    w = smilImageView(im)
    windows.append(w)
    g.register(w.uuid, w)

  print()
  g.list()

  if True:
    r = input("Type any key to continue")
    return r
  else:
    return app.exec_()


# =============================================================================
#
#
if __name__ == '__main__':
  import sys

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

