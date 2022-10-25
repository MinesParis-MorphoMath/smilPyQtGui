#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  smilPyQtDlog.py
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

import argparse as ap
import configparser as cp

import math as m
import numpy as np

#import pandas      as pd #import statistics  as st #import scipy.stats as sst
#import seaborn     as sb

import smilPython as sp

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QScrollArea, QMessageBox,
                             QMainWindow, QMenu, QAction, qApp, QFileDialog,
                             QStatusBar, QTextEdit, QWidget, QDialog,
                             QGraphicsView, QGraphicsScene, QSlider, QLineEdit,
                             QPushButton)
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout

import smilPyQtTools as spqt

# -----------------------------------------------------------------------------
#
#
debug = False
verbose = False


def InfoMessageDialog(title=None, text=None):
  msgbox = QMessageBox()
  msgbox.setWindowTitle(title)
  title = '<center><b>' + title + '</b></center>'

  msgbox.setText(title)
  msgbox.setInformativeText(text)
  msgbox.exec()


# =============================================================================
#
#  #    #    #  ######   ####
#  #    ##   #  #       #    #
#  #    # #  #  #####   #    #
#  #    #  # #  #       #    #
#  #    #   ##  #       #    #
#  #    #    #  #        ####
#
def smilImageInfo(win=None):
  title = 'Image information'

  size = win.image.getSize()[0:win.image.getDimension()]
  sl = [
    '<center>', '<pre>', 'Name       : {:}'.format(win.image.getName()),
    'Data type  : {:}'.format(win.image.getTypeAsString()),
    'Dimensions : {:}'.format(win.image.getDimension()),
    'Size       : {:}'.format(size),
    'Allocated  : {:} bytes'.format(win.image.getAllocatedSize()), '',
    'ID         : {:}'.format(win.uuid), '</pre>', '</center>'
  ]

  mLen = 0
  for s in sl:
    mLen = max(mLen, len(s))
  for i in range(len(sl)):
    sl[i] = sl[i].ljust(mLen + 4)
  sOut = '\n'.join(sl)

  InfoMessageDialog(title, sOut)


#
#   ####   ######   #####    #    #    ##    #    #  ######
#  #    #  #          #      ##   #   #  #   ##  ##  #
#  #       #####      #      # #  #  #    #  # ## #  #####
#  #  ###  #          #      #  # #  ######  #    #  #
#  #    #  #          #      #   ##  #    #  #    #  #
#   ####   ######     #      #    #  #    #  #    #  ######
#
class smilGetImageName(QDialog):
  def __init__(self):
    super().__init__()
    self.initializeUI()

  def initializeUI(self):
    self.setMaximumSize(310, 200)
    self.setWindowTitle("Set image name")

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    label = QLabel()
    label.setText("Enter a new name for this image...")

    self.name_edit = QLineEdit()

    cancel_button = QPushButton("Cancel", self)
    cancel_button.move(140, 90)
    cancel_button.clicked.connect(self.cancel)

    accept_button = QPushButton("OK", self)
    accept_button.move(210, 90)
    accept_button.clicked.connect(self.accept)

    hbox = QHBoxLayout()
    hbox.addWidget(cancel_button)
    hbox.addWidget(accept_button)

    vbox = QVBoxLayout()
    vbox.addWidget(label)
    vbox.addWidget(self.name_edit)
    vbox.addLayout(hbox)

    self.setLayout(vbox)
    return

    QLabel("Enter a new name for this image...", self).move(70, 10)
    name_label = QLabel("Name:", self)
    name_label.move(20, 50)

    self.name_edit = QLineEdit(self)
    self.name_edit.resize(210, 20)
    self.name_edit.move(70, 50)

    cancel_button = QPushButton("Cancel", self)
    cancel_button.move(140, 90)
    cancel_button.clicked.connect(self.cancel)

    accept_button = QPushButton("OK", self)
    accept_button.move(210, 90)
    accept_button.clicked.connect(self.accept)

  def cancel(self):
    self.result = ""
    self.close()

  def accept(self):
    self.result = self.name_edit.text()
    self.close()

  def getName(self):
    self.exec()
    return self.result


if __name__ == '__main__':
  import sys

  # sys.exit(main(cli, config, sys.argv))
