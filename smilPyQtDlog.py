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
                             QPushButton, QListWidget, QListWidgetItem)
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout

from PyQt5 import Qwt

import smilPyQtTools as spqt

# -----------------------------------------------------------------------------
#
#
debug = False
verbose = False


# =============================================================================
#
#
class HelpDialog(QDialog):
  def __init__(self, align=Qt.AlignLeft):
    super().__init__()

    message = ''
    icon = None
    align = Qt.AlignLeft

    toc = """
1. Menu Image
2. Menu View
3. Menu Tools
4. Menu Help
    """

    message = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus cursus nisi non quam feugiat pellentesque. In porta risus non mauris tincidunt varius. Pellentesque semper sapien at tincidunt tempor. Donec sit amet viverra sem, vitae porta nulla. Integer turpis dolor, aliquet et nisi ac, blandit viverra erat. Aenean commodo ipsum diam, sed suscipit risus dignissim et. Donec sed felis at diam feugiat dapibus. Nullam tincidunt non ipsum eget convallis. Fusce sed quam dignissim, suscipit ligula eu, volutpat dui. Cras pellentesque rutrum ex in posuere.

Sed fermentum vel nisl eu finibus. Nullam ante orci, posuere a eros vel, imperdiet sollicitudin justo. Ut blandit magna in volutpat facilisis. Proin vel erat arcu. Vivamus dignissim consequat massa ac consectetur. Quisque accumsan dolor sed commodo tristique. Fusce porta viverra augue quis tempor. Sed eget tortor sed erat viverra ultrices sit amet vitae lorem. Aliquam porta congue orci at imperdiet. Vivamus molestie ipsum eget ipsum hendrerit, vitae molestie nulla efficitur. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam eget est odio. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut orci lacus, tempor vitae dignissim non, imperdiet in arcu.

Nulla eget ex accumsan, accumsan risus sed, varius tellus. Nam dictum placerat erat quis tristique. Pellentesque metus ex, dictum a quam a, congue viverra eros. Etiam cursus facilisis urna sed imperdiet. Fusce at venenatis leo. Proin nec massa nisi. Morbi semper mollis enim, eu luctus ipsum vehicula sed. Sed vulputate, mauris nec ultrices pellentesque, augue nulla rutrum mauris, eu consectetur purus dolor sit amet lacus. Pellentesque nec turpis eros.

Nulla vitae elit arcu. Fusce vel libero vitae magna varius congue vel commodo dui. Maecenas et felis non ex facilisis bibendum accumsan at felis. Fusce sodales auctor tortor, ultrices mollis quam luctus a. Donec consectetur arcu turpis. Suspendisse dui ante, pharetra sit amet lorem quis, cursus euismod massa. Mauris iaculis faucibus ipsum id lobortis. Aenean bibendum neque quis nunc malesuada lobortis. Sed in commodo arcu, a molestie velit. Praesent luctus orci non metus finibus vulputate. Quisque aliquam venenatis urna vel bibendum. Fusce interdum, diam quis vehicula sagittis, lorem nulla semper velit, id bibendum lacus eros eu lectus. Ut tincidunt ultricies sem. Suspendisse nibh eros, facilisis a nibh sit amet, mattis tristique leo. Curabitur id interdum ex. Cras ut neque maximus, pellentesque diam vitae, pharetra leo.

Curabitur sed sollicitudin felis. Nullam eu odio sed purus lacinia fringilla. Nulla lorem massa, dignissim vitae pulvinar varius, eleifend vitae urna. Sed dui nisl, laoreet aliquet efficitur quis, eleifend at lacus. Fusce suscipit posuere arcu, nec commodo dolor viverra ut. Fusce eget pharetra lectus. Donec iaculis luctus vehicula. Cras rutrum varius tincidunt. Donec auctor tortor eu nibh venenatis euismod. Interdum et malesuada fames ac ante ipsum primis in faucibus.
    """

    self.title = "<h3>Help smilPyQtGui </h3>"
    if isinstance(message, list):
      self.message = '\n'.join(message)
    else:
      self.message = message
    self.toc = toc
    self.icon = icon
    self.align = align

    self.initializeUI()

  def initializeUI(self):
    self.setMinimumSize(384, 200)
    self.setWindowTitle(self.title)

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    label = QLabel()
    label.setText(self.title)
    label.setAlignment(Qt.AlignCenter)

    table = QTextEdit()
    table.setText(self.toc)
    table.setAlignment(self.align)
    #table.setStyleSheet("border : 1px solid black;")
    #table.setWordWrap(True)
    table.setReadOnly(True)
    table.setFixedWidth(140)

    content = QTextEdit()
    content.setText(self.message)
    content.setAlignment(self.align)
    #content.setStyleSheet("border : 1px solid black;")
    #content.setWordWrap(True)
    content.setReadOnly(True)
    content.setMinimumWidth(240)

    body_layout = QHBoxLayout()
    body_layout.addWidget(table)
    body_layout.addWidget(content)

    ok_button = QPushButton("OK")
    ok_button.clicked.connect(self.ok)

    buttons_layout = QHBoxLayout()
    buttons_layout.addStretch()
    buttons_layout.addWidget(ok_button)

    tout = QVBoxLayout()
    tout.addWidget(label)
    tout.addLayout(body_layout)
    #tout.addStretch()
    tout.addLayout(buttons_layout)

    self.setLayout(tout)

  def ok(self):
    self.close()

  def run(self):
    self.exec()



# =============================================================================
#
#
class InfoDialog(QDialog):
  def __init__(self, title='', message=None, icon=None, align=Qt.AlignLeft):
    super().__init__()
    self.title = title
    if isinstance(message, list):
      self.message = '\n'.join(message)
    else:
      self.message = message
    self.icon = icon
    self.align = align

    self.initializeUI()

  def initializeUI(self):
    self.setMinimumSize(384, 100)
    self.setWindowTitle(self.title)

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    label = QLabel()
    label.setText(self.title)
    label.setAlignment(Qt.AlignCenter)

    message = QLabel()
    message.setText(self.message)
    message.setAlignment(self.align)
    #message.setStyleSheet("border : 1px solid black;")
    message.setWordWrap(True)

    all_layout = QVBoxLayout()
    all_layout.addWidget(label)
    all_layout.addWidget(message)

    ok_button = QPushButton("OK")
    ok_button.clicked.connect(self.ok)

    buttons_layout = QHBoxLayout()
    buttons_layout.addStretch()
    buttons_layout.addWidget(ok_button)

    tout = QVBoxLayout()
    tout.addLayout(all_layout)
    tout.addStretch()
    tout.addLayout(buttons_layout)

    self.setLayout(tout)

  def ok(self):
    self.close()

  def run(self):
    self.exec()

def ShowInfoDialog(title='', message='', align=Qt.AlignCenter):
  idlog = InfoDialog(title, message, align)
  idlog.run()

# =============================================================================
#
#
def InfoMessageDialog(title=None, message=None):
  msgbox = QMessageBox()
  msgbox.setWindowTitle(title)
  title = '<center><b>' + title + '</b></center>'
  msgbox.setText(title)
  msgbox.setInformativeText(message)
  msgbox.exec()

# =============================================================================
#
#
def InfoNotYet(message=None):
  if message is None:
    message = "Not Yet Implemented"
  InfoMessageDialog("Not Yet Implemented", message)

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

# =============================================================================
#
#  #       #  #    #  #    #        #  #    #    ##     ####   ######   ####
#  #       #  ##   #  #   #         #  ##  ##   #  #   #    #  #       #
#  #       #  # #  #  ####          #  # ## #  #    #  #       #####    ####
#  #       #  #  # #  #  #          #  #    #  ######  #  ###  #            #
#  #       #  #   ##  #   #         #  #    #  #    #  #    #  #       #    #
#  ######  #  #    #  #    #        #  #    #  #    #   ####   ######   ####
#
class MItem(QListWidgetItem):
  def __init__(self, key, data):
    super().__init__()
    self.key = key
    self.data = data

  def text(self):
    return '{:5s} {:s}'.format(self.key, self.data.imName)

class LinkImagesDialog(QDialog):
  def __init__(self, imName='', All={}, Linked={}):
    super().__init__()

    if imName != '':
      self.imName = imName
    else:
      self.imName = 'No Name'
    self.All = All
    self.Linked = Linked
    self.rLinked = {}
    self.ok = False

    self.initializeUI()

  def initializeUI(self):
    """Set up the application's GUI."""
    self.setMinimumSize(400, 200)
    self.setWindowTitle(self.imName)

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    """Create and arrange widgets in the main window."""

    label = QLabel()
    label.setText('<h3><b>' + "Images linked to " + self.imName + '</b></h3>')
    label.setAlignment(Qt.AlignCenter)

    # Availlable images"
    lbl_all = QLabel("All images")
    lbl_all.setAlignment(Qt.AlignCenter)

    self.list_all = QListWidget()
    self.list_all.setAlternatingRowColors(True)

    for item in self.All.keys():
      if item in self.Linked:
        continue
      list_item = QListWidgetItem()
      data = MItem(item, self.All[item])
      list_item.data = data
      list_item.setText(data.text())
      self.list_all.addItem(list_item)

    all_layout = QVBoxLayout()
    all_layout.addWidget(lbl_all)
    all_layout.addWidget(self.list_all)

    # Linked images
    lbl_lnk = QLabel("Linked images")
    lbl_lnk.setAlignment(Qt.AlignCenter)

    self.list_link = QListWidget()
    self.list_link.setAlternatingRowColors(True)

    for item in self.Linked.keys():
      list_item = QListWidgetItem()
      data = MItem(item, self.Linked[item])
      list_item.data = data
      list_item.setText(data.text())
      self.list_link.addItem(list_item)

    lnk_layout = QVBoxLayout()
    lnk_layout.addWidget(lbl_lnk)
    lnk_layout.addWidget(self.list_link)

    add_button = QPushButton(">>")
    add_button.clicked.connect(self.addListItem)

    remove_button = QPushButton("<<")
    remove_button.clicked.connect(self.removeOneItem)

    buttons_layout = QVBoxLayout()
    buttons_layout.addWidget(add_button)
    buttons_layout.addWidget(remove_button)

    list_layout = QHBoxLayout()
    list_layout.addLayout(all_layout)
    list_layout.addLayout(buttons_layout)
    list_layout.addLayout(lnk_layout)

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(self.cancel)
    accept_button = QPushButton("OK")
    accept_button.clicked.connect(self.accept)

    vbuttons_layout = QHBoxLayout()
    vbuttons_layout.addStretch()
    vbuttons_layout.addWidget(cancel_button)
    vbuttons_layout.addWidget(accept_button)

    tout = QVBoxLayout()
    tout.addWidget(label)
    tout.addLayout(list_layout)
    tout.addLayout(vbuttons_layout)

    self.setLayout(tout)

  def addListItem(self):
    """Add a single item to the list widget."""
    rowa = self.list_all.currentRow()
    rowl = self.list_link.currentRow()
    if rowa < 0:
      return

    allItem = self.list_all.currentItem()
    data = allItem.data
    lnkItem = QListWidgetItem(allItem)
    lnkItem.data = data
    self.list_link.addItem(lnkItem)

    row = self.list_all.currentRow()
    item = self.list_all.takeItem(row)
    del item

  def removeOneItem(self):
    """Remove a single item from the list widget."""
    rowa = self.list_all.currentRow()
    rowl = self.list_link.currentRow()
    if rowl < 0:
      return

    lnkItem = self.list_link.currentItem()
    data = lnkItem.data
    allItem = QListWidgetItem(lnkItem)
    allItem.data = data
    self.list_all.addItem(allItem)

    row = self.list_link.currentRow()
    item = self.list_link.takeItem(row)
    del item

  def cancel(self):
    self.close()

  def accept(self):
    self.getLinkedList()
    self.ok = True
    self.close()

  def getLinkedList(self):
    self.rLinked = {}
    l = self.list_link
    for i in range(0, l.count()):
      data = l.item(i).data
      self.rLinked[data.key] = data.data

  def run(self):
    self.exec()
    return self.rLinked, self.ok

# =============================================================================
#
#  #        #    ####    #####       #   #    #    ##     ####   ######   ####
#  #        #   #          #         #   ##  ##   #  #   #    #  #       #
#  #        #    ####      #         #   # ## #  #    #  #       #####    ####
#  #        #        #     #         #   #    #  ######  #  ###  #            #
#  #        #   #    #     #         #   #    #  #    #  #    #  #       #    #
#  ######   #    ####      #         #   #    #  #    #   ####   ######   ####
#
class MItem(QListWidgetItem):
  def __init__(self, key, data):
    super().__init__()
    self.key = key
    self.data = data

  def text(self):
    return '{:5s} {:s}'.format(self.key, self.data.imName)

class ListImagesDialog(QDialog):
  def __init__(self, All={}):
    super().__init__()
    self.All = All
    self.ok = False

    self.initializeUI()

  def initializeUI(self):
    """Set up the application's GUI."""
    self.setMinimumSize(400, 200)
    self.setWindowTitle("Images")

    self.setUpMainWindow()
    self.show()

  def setUpMainWindow(self):
    """Create and arrange widgets in the main window."""

    # Availlable images"
    lbl_all = QLabel("All images")
    lbl_all.setAlignment(Qt.AlignCenter)

    self.list_all = QListWidget()
    self.list_all.setAlternatingRowColors(True)

    for item in self.All.keys():
      list_item = QListWidgetItem()
      data = MItem(item, self.All[item])
      list_item.data = data
      list_item.setText(data.text())
      self.list_all.addItem(list_item)

    all_layout = QVBoxLayout()
    all_layout.addWidget(lbl_all)
    all_layout.addWidget(self.list_all)

    list_layout = QHBoxLayout()
    list_layout.addLayout(all_layout)
    accept_button = QPushButton("OK")
    accept_button.clicked.connect(self.accept)

    vbuttons_layout = QHBoxLayout()
    vbuttons_layout.addStretch()
    vbuttons_layout.addWidget(accept_button)

    tout = QVBoxLayout()
    tout.addLayout(list_layout)
    tout.addLayout(vbuttons_layout)

    self.setLayout(tout)

  def accept(self):
    self.ok = True
    self.close()

  def run(self):
    self.exec()

# =============================================================================
#
#  #    #     #     ####    #####   ####    ####   #####     ##    #    #
#  #    #     #    #          #    #    #  #    #  #    #   #  #   ##  ##
#  ######     #     ####      #    #    #  #       #    #  #    #  # ## #
#  #    #     #         #     #    #    #  #  ###  #####   ######  #    #
#  #    #     #    #    #     #    #    #  #    #  #   #   #    #  #    #
#  #    #     #     ####      #     ####    ####   #    #  #    #  #    #
#
class smilHistogram(QDialog):
  def __init__(self, view, x, y):
    super().__init__()

    self.view = view
    self.title = view.imName
    self.x = np.array(x)
    self.y = np.array(y)

    self.mousePosition = QPoint(0, 0)

    self.initializeUI()

  def initializeUI(self):
    #self.setMaximumSize(310, 130)
    #self.setSize(400,300)
    self.setMinimumSize(400, 300)

    self.setWindowTitle(self.title)

    self.setUpMainWindow()
    self.setMouseTracking(True)

    self.show()

  def setUpMainWindow(self):

    label = QLabel()
    label.setText('<h4>' + "Histogram : " + self.title + '</h4>')
    label.setAlignment(Qt.AlignCenter)

    self.plot = Qwt.QwtPlot(self)
    #self.plot.setTitle("Histogram\n" + self.title)
    self.plot.setCanvasBackground(Qt.white)
    #self.plot.insertLegend( Qwt.QwtLegend() )
    self.plot.setMouseTracking(True)

    self.grid = Qwt.QwtPlotGrid()
    self.grid.attach(self.plot)

    curveSin = Qwt.QwtPlotCurve()
    #curveSin.setTitle("Some Points")
    curveSin.setPen(Qt.red, 1)
    curveSin.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, True)

#    curveCos = Qwt.QwtPlotCurve()
    #curveCos.setTitle("Some Points")
#    curveCos.setPen(Qt.red, 1)
#    curveCos.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased, True)

    #symbol = Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse, QBrush(Qt.yellow),
    #                       QPen(Qt.red, 2), QSize(8, 8))
    #curve.setSymbol(symbol)

    #x = np.arange(0, 10, 0.1)
    #y = np.sin(x)
    #z = np.cos(x)
    curveSin.setSamples(self.x, self.y)
    curveSin.attach(self.plot)
    #curveCos.setSamples(x, z)
    #curveCos.attach(self.plot)

    xmax = self.view.image.getDataTypeMax()
    self.plot.setAxisScale(Qwt.QwtPlot.xBottom, -1, xmax + 1, (xmax + 1) // 8)

    zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom, Qwt.QwtPlot.yLeft,
                               self.plot.canvas())
    zoomer.setZoomBase(False)
    zoomer.zoom(0)

    self.plot.resize(600,400)
    self.plot.replot()
    self.plot.show()

    accept_button = QPushButton("OK", self)
    #accept_button.move(210, 90)
    accept_button.clicked.connect(self.accept)

    hbox = QHBoxLayout()
    hbox.addStretch()
    hbox.addWidget(accept_button)

    vbox = QVBoxLayout()
    vbox.addWidget(label)
    vbox.addWidget(self.plot)
    vbox.addLayout(hbox)

    self.setLayout(vbox)

  #
  #   E V E N T S
  #
  def mouseMoveEvent(self, event):
    self.mousePosition = event.pos()
    x = int(self.mousePosition.x() + 0)
    y = int(self.mousePosition.y() + 0)
    #print("mouse : {:d} {:d}".format(x, y))

  def accept(self):
    self.close()

  def run(self):
    self.exec()

# =============================================================================
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
