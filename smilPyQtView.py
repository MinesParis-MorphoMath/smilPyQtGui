#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  smilPyQtGui.py
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

import math as m
import numpy as np

import smilPython as sp

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon, QColor, qRgb
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import (QLabel, QSizePolicy, QScrollArea, QMessageBox,
                             QMainWindow, QMenu, QAction, qApp, QFileDialog,
                             QInputDialog, QStatusBar, QTextEdit, QWidget,
                             QDialog, QGraphicsView, QGraphicsScene, QSlider,
                             QLineEdit)
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout

import smilPyQtDlog as spqd

from smilPyQtGui import *

# -----------------------------------------------------------------------------
#
#
debug = False
verbose = False

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
#   ####    ####   ######  #    #  ######
#  #       #    #  #       ##   #  #
#   ####   #       #####   # #  #  #####
#       #  #       #       #  # #  #
#  #    #  #    #  #       #   ##  #
#   ####    ####   ######  #    #  ######
#
class smilGraphicsView(QGraphicsView):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent
    width, height = parent.width(), parent.height()

    self.baseColorTable = []
    self.rainbowColorTable = []
    self.labelColorTable = []
    self.showLabel = False
    self.initColorTables()

    self.qScene = QGraphicsScene()
    self.setScene(self.qScene)
    self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    self.setMouseTracking(True)

    self.show()

  #
  # I M A G E
  #
  def smilToNumpyImage(self, image=None, z=0):
    parent = self.parent
    image = parent.image

    uLim = image.getDataTypeMax()
    lLim = image.getDataTypeMin()
    Max = sp.maxVal(image)
    Min = sp.minVal(image)
    if Max == Min:
      Max = uLim
      Min = lLim

    if parent.autorange:
      coeff = 255. / (Max - Min)
    else:
      coeff = 255. / (uLim - lLim)

    w = image.getWidth()
    h = image.getHeight()
    d = image.getDepth()
    #w -= w % 4
    #h -= h % 4
    # print('  imt : {:4d} {:4d} {:4d}'.format(w, h, d))
    imArray = np.zeros((h, w), dtype=sp2npTypes[parent.imType])
    for i in range(0, w):
      for j in range(0, h):
        imArray[j, i] = int(coeff * image.getPixel(i, j, z))
    return imArray

  #
  #
  #
  def setImage(self):
    parent = self.parent

    self.imArray = self.smilToNumpyImage(z=parent.curSlice)
    self.qImage = QImage(self.imArray, self.imArray.shape[1],
                         self.imArray.shape[0], QImage.Format_Indexed8)

    if self.showLabel:
      self.qImage.setColorTable(self.labelColorTable)
    else:
      self.qImage.setColorTable(self.baseColorTable)

    self.qPixmap = QPixmap.fromImage(self.qImage)
    self.qScene.addPixmap(self.qPixmap)

  def update(self, factor=1., sliderChanged=False, colorTableChanged=False):
    parent = self.parent

    if sliderChanged or colorTableChanged:
      self.setImage()

    if factor > 0 and factor != 1:
      self.scale(factor, factor)
      parent.scaleValue *= factor

      if debug:
        print("scaleValue : {:.3f}".format(parent.scaleValue))
        print("sceneRect   : {:}".format(self.sceneRect()))

    if factor == 0.:
      factor = 1. / parent.scaleValue
      self.scale(factor, factor)
      parent.scaleValue = 1.

      if debug:
        print("scaleValue : {:.3f}".format(parent.scaleValue))
        print("sceneRect   : {:}".format(self.sceneRect()))

    if debug:
      print("viewRect    : {:} {:}".format(self.width(), self.height()))

    hb = self.horizontalScrollBar().value()
    vb = self.verticalScrollBar().value()
    if debug:
      print("Scroll bar : {:d} {:d}".format(hb, vb))

    #self.qScene.update(self.qRect)

  def initColorTables(self):
    for i in range(0, 256):
      self.baseColorTable.append(qRgb(i, i, i))
    self.rainbowColorTable = []
    for i in range(0, 256):
      self.rainbowColorTable.append(QColor.fromHsvF(i / 256., 1.0, 1.0).rgb())

    self.labelColorTable.append(qRgb(0, 0, 0))
    curC = 0
    for i in range(0, 255):
      self.labelColorTable.append(self.rainbowColorTable[curC])
      curC = (curC + 47) % 256

  #
  # U I
  #
  def getScrollValues(self):
    hb = self.horizontalScrollBar().value()
    vb = self.verticalScrollBar().value()
    if debug:
      print("Scroll bar : {:d} {:d}".format(hb, vb))
    return (hb, vb)

  #
  #   E V E N T S
  #
  def mouseMoveEvent(self, event):
    parent = self.parent
    parent.mousePosition = event.pos()
    parent.updateViewHint()


# =============================================================================
#
#  #    #    ##       #    #    #
#  ##  ##   #  #      #    ##   #
#  # ## #  #    #     #    # #  #
#  #    #  ######     #    #  # #
#  #    #  #    #     #    #   ##
#  #    #  #    #     #    #    #
#
class smilQtView(QMainWindow):
  def __init__(self, img=None, name=None):
    super().__init__()

    if img is None:
      return

    uuid = smGui.register(self)
    if uuid is None:
      uuid = str(uuid)
    self.uuid = uuid

    self.initializeMembers()
    self.initializeUI()

    self.setupImage(img)
    self.resize(self.w + 20, self.h + 100)

    self.setMouseTracking(True)
    self.show()

  #
  #
  #
  def initializeMembers(self):
    self.scaleValue = 1.
    self.scaleMax = 12.
    self.showLabel = False
    self.autorange = False

    self.image = None
    self.imType = ''
    self.w = 0
    self.h = 0
    self.d = 0
    self.curSlice = 0
    self.imName = ''

    self.title = '{:s} - {:s}'.format(self.uuid, self.imName)

    self.linkedImages = {}

    self.mousePosition = QPoint(0, 0)
    self.lastPosition = QPoint(0, 0)

  #
  #
  #
  def initializeUI(self):
    """Set up the application's GUI."""
    self.setMinimumSize(200, 200)
    #self.resize(self.w, self.h)

    self.setTitle()
    self.setUpMainWindow()
    self.createActions()
    self.createMenu()

  #
  #
  #
  def setUpMainWindow(self):

    self.lbl1 = QLabel()
    self.lbl1.setText("Label 1")

    self.slider = QSlider()
    self.slider.setOrientation(Qt.Horizontal)
    self.slider.setMinimum(0)
    self.slider.setMaximum(99)
    self.slider.setTracking(True)
    self.slider.valueChanged[int].connect(self.sliderValueChanged)
    self.slider.setVisible(False)

    self.smScene = smilGraphicsView(self)

    vbox = QVBoxLayout()
    vbox.addWidget(self.lbl1)
    vbox.addWidget(self.slider)
    vbox.addWidget(self.smScene)

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
    image_menu = self.menuBar().addMenu("Image")
    image_menu.addAction(self.list_act)
    image_menu.addAction(self.hide_act)

    image_menu.addSeparator()
    image_menu.addAction(self.setName_act)
    image_menu.addAction(self.reload_act)

    image_menu.addSeparator()
    image_menu.addAction(self.save_act)
    image_menu.addAction(self.print_act)

    image_menu.addSeparator()
    image_menu.addAction(self.close_act)

    # Create View menu and add actions
    view_menu = self.menuBar().addMenu("View")
    view_menu.addAction(self.zoomIn_act)
    view_menu.addAction(self.zoomOut_act)
    view_menu.addAction(self.zoomReset_act)
    view_menu.addSeparator()
    view_menu.addAction(self.magnify_act)
    view_menu.addSeparator()
    view_menu.addAction(self.label_act)

    # Create Tools menu
    tools_menu = self.menuBar().addMenu("Tools")
    tools_menu.addAction(self.link_act)
    tools_menu.addSeparator()
    tools_menu.addAction(self.histogram_act)
    tools_menu.addAction(self.info_act)

    # Create Help menu
    help_menu = self.menuBar().addMenu("Help")
    help_menu.addAction(self.help_act)
    help_menu.addSeparator()
    help_menu.addAction(self.about_act)
    help_menu.addAction(self.aboutqt_act)

  def createActions(self):
    """Create the application's menu actions."""

    #
    # File menu
    #
    self.list_act = QAction(QIcon("images/open_file.png"), "Views manager")
    #self.list_act.setShortcut("Ctrl+S")
    self.list_act.setStatusTip("Views manager")
    self.list_act.triggered.connect(self.fn_list)

    self.setName_act = QAction(QIcon("images/save_file.png"), "Set image name")
    #self.setName_act.setShortcut("Ctrl+R")
    self.setName_act.setStatusTip("Set image Name")
    self.setName_act.triggered.connect(self.fn_setname)

    self.reload_act = QAction(QIcon("images/save_file.png"), "Reload image")
    self.reload_act.setShortcut("Ctrl+R")
    self.reload_act.setStatusTip("Reload Image")
    self.reload_act.triggered.connect(self.fn_reload)

    self.save_act = QAction(QIcon("images/save_file.png"), "Save Snapshot")
    self.save_act.setShortcut("Ctrl+S")
    self.save_act.setStatusTip("Save Snapshot")
    self.save_act.triggered.connect(self.fn_save)

    self.print_act = QAction(QIcon("images/print.png"), "Print")
    self.print_act.setShortcut("Ctrl+P")
    self.print_act.setStatusTip("Print image")
    self.print_act.triggered.connect(self.fn_print)
    #self.print_act.setEnabled(False)

    self.hide_act = QAction(QIcon("images/exit.png"), "Hide")
    self.hide_act.setShortcut("Ctrl+Q")
    self.hide_act.setStatusTip("Hide Window")
    self.hide_act.triggered.connect(self.fn_hide)

    self.close_act = QAction(QIcon("images/exit.png"), "Close")
    self.close_act.setShortcut("Ctrl+W")
    self.close_act.setStatusTip("Close Window")
    self.close_act.triggered.connect(self.fn_close)

    #
    # View menu
    #
    self.zoomIn_act = QAction("Zoom In")
    self.zoomIn_act.setShortcut("Ctrl++")
    self.zoomIn_act.setStatusTip("Zoom In image")
    self.zoomIn_act.triggered.connect(self.fn_zoomIn)

    self.zoomOut_act = QAction("Zoom Out")
    self.zoomOut_act.setShortcut("Ctrl+-")
    self.zoomOut_act.setStatusTip("Zoom Out image")
    self.zoomOut_act.triggered.connect(self.fn_zoomOut)

    self.zoomReset_act = QAction("Normal size")
    self.zoomReset_act.setShortcut("Ctrl+=")
    self.zoomReset_act.setStatusTip("Reset Zoom to Original")
    self.zoomReset_act.triggered.connect(self.fn_zoomReset)

    self.magnify_act = QAction("Magnify ...")
    self.magnify_act.setShortcut("Ctrl+M")
    self.magnify_act.setStatusTip("Close look around pointer")
    self.magnify_act.triggered.connect(self.fn_magnify)

    self.label_act = QAction("Toggle show image as label")
    self.label_act.setShortcut("Ctrl+L")
    self.label_act.setStatusTip("Show labelled image")
    self.label_act.triggered.connect(self.fn_label)

    self.info_act = QAction("Image information")
    self.info_act.setShortcut("Ctrl+I")
    self.info_act.setStatusTip("Image information")
    self.info_act.triggered.connect(self.fn_info)

    self.histogram_act = QAction("Histogram")
    #self.histogram_act.setShortcut("Ctrl+I")
    self.histogram_act.setStatusTip("Show image histogram")
    self.histogram_act.triggered.connect(self.fn_histogram)

    #
    # Tools menu
    #
    self.link_act = QAction("Link configuration...")
    #self.link_act.setShortcut("Ctrl+L")
    self.link_act.setStatusTip("Configure Linked images")
    self.link_act.triggered.connect(self.fn_link)

    #
    # Help menu
    #
    self.help_act = QAction("Help")
    self.help_act.setStatusTip("Help")
    self.help_act.triggered.connect(self.fn_help)

    self.about_act = QAction("About smilPyQtGui")
    self.about_act.setStatusTip("About smilPyQtGui")
    self.about_act.triggered.connect(self.fn_about)

    self.aboutqt_act = QAction("About Qt")
    self.aboutqt_act.setStatusTip("About Qt")
    self.aboutqt_act.triggered.connect(self.fn_aboutqt)

  #
  #
  #
  def setTitle(self, imName=None):
    if not imName is None:
      self.imName = imName
    self.title = 'ID {:s} - {:s}'.format(self.uuid, self.imName)
    self.setWindowTitle(self.title)

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
    self.setTitle()

    self.slider.setMinimum(0)
    self.slider.setMaximum(self.d - 1)
    if self.d > 1:
      self.slider.setVisible(True)

    self.smScene.setImage()
    self.update()

    fmt = "Image : {:6s} : w({:d}) h({:d}) d({:d})"
    print(fmt.format(self.imType, self.w, self.h, self.d))

  #
  def update(self, factor=1., sliderChanged=False, colorTableChanged=False):
    self.smScene.update(factor, sliderChanged, colorTableChanged)
    #self.resize(self.w * self.scale + 20, self.h * self.scale + 80)

    self.updateViewHint()
    return

  #
  # EVENT HANDLERS
  #
  def isInImage(self, x, y):
    if x < 0 or x >= self.w:
      return False
    if y < 0 or y >= self.h:
      return False
    return True

  def updateViewHint(self):
    dx, dy = self.smScene.getScrollValues()
    x = int(self.mousePosition.x() + dx)
    y = int(self.mousePosition.y() + dy)

    x = int(x // self.scaleValue)
    y = int(y // self.scaleValue)

    s = []
    s.append("Scale : {:5.1f} %".format(100 * self.scaleValue))
    if self.d > 1:
      s.append("Slice : {:d}".format(self.curSlice))

    if self.isInImage(x, y):
      v = self.image.getPixel(x, y, self.curSlice)
      s.append("Mouse : ({:4d}, {:4d})".format(x, y))
      s.append("Pixel value : {}".format(v))

    sOut = " - ".join(s)
    self.lbl1.setText(sOut)

    # update linked images
    for k in self.linkedImages.keys():
      view = self.linkedImages[k]
      uuid = view.uuid
      if not smGui.isRegistered(uuid):
        del self.linkedImages[k]
      view.updateViewHintFromOther(x, y)

  def updateViewHintFromOther(self, x, y):
    s = []
    s.append("Scale : {:5.1f} %".format(100 * self.scaleValue))
    if self.d > 1:
      s.append("Slice : {:d}".format(self.curSlice))

    if self.isInImage(x, y):
      v = self.image.getPixel(x, y, self.curSlice)
      s.append("Mouse : ({:4d}, {:4d})".format(x, y))
      s.append("Pixel value : {}".format(v))

    sOut = " - ".join(s)
    self.lbl1.setText(sOut)

  def updateSliderFromOther(self, sliderValue):
    self.slider.setSliderPosition(sliderValue)
    self.curSlice = sliderValue
    self.update(sliderChanged=True)

  #
  # I M A G E   M E N U
  #
  def fn_list(self):
    smGui.viewManager()
    return

  def fn_setname(self):
    newName = spqd.smilGetImageName(self.imName).getName()
    if not newName is None and newName != '':
      self.image.setName(newName)
      self.imName = newName
      self.setTitle()

  def fn_reload(self):
    self.setupImage(self.image)

  def fn_save(self):
    self.saveImage()

  def fn_print(self):
    self.printImage()

  def fn_hide(self):
    self.hide()

  def fn_close(self):
    smGui.unregister(self.uuid)
    self.close()

  #
  #
  # V I E W   M E N U
  #
  def fn_zoomIn(self):
    fInc = 1.25
    s = self.scaleValue * fInc
    if s < self.scaleMax:
      self.update(factor=1.25)

  def fn_zoomOut(self):
    fDec = 0.8
    s = self.scaleValue * fDec
    if s * self.scaleMax > 1.:
      self.update(factor=0.8)

  def fn_zoomReset(self):
    self.update(factor=0.)

  def fn_label(self):
    self.smScene.showLabel = not self.smScene.showLabel
    self.update(colorTableChanged=True)
    pass

  def fn_magnify(self):
    print(inspect.stack()[0][3])
    spqd.InfoNotYet()
    pass

  #
  #  T O O L S   M E N U
  #
  def fn_link(self):
    #dictAll = spqt.SRegister.list()
    dictAll = smGui.getCopy()
    dictLnk = self.linkedImages
    dictTmp = {}
    for k in dictAll.keys():
      dictTmp[k] = dictAll[k]
    w = spqd.LinkImagesDialog(self, dictTmp, dictLnk)
    dictLnkT, ok = w.run()
    if ok:
      self.linkedImages = {}
      for k in dictLnkT.keys():
        self.linkedImages[k] = dictLnkT[k]

  def fn_histogram(self):
    histoMap = sp.histogram(self.image)
    x = histoMap.keys()
    y = histoMap.values()
    spqd.smilHistogram(self, x, y).run()
    if verbose:
      for k in histoMap:
        if histoMap[k] == 0:
          continue
        print('  {:3d} {:6d}'.format(k, histoMap[k]))

  def fn_info(self):
    size = self.image.getSize()
    Min = sp.minVal(self.image)
    Max = sp.maxVal(self.image)
    mean, stdev = sp.meanVal(self.image)
    median = sp.medianVal(self.image)

    infos = []
    infos.append(['View ID', '{:}'.format(self.uuid)])

    infos.append(['Name', '{:}'.format(self.image.getName())])
    infos.append(['Data type', '{:}'.format(self.image.getTypeAsString())])
    infos.append(['Dimensions', '{:}'.format(self.image.getDimension())])
    infos.append(['Size (w x h x d)', '{:}'.format(size)])
    infos.append(
      ['Allocated', '{:} bytes'.format(self.image.getAllocatedSize())])

    infos.append(['Binary image', '{:}'.format(sp.isBinary(self.image))])
    infos.append(
      ['Values count', '{:d}'.format(len(sp.valueList(self.image, False)))])
    infos.append(['Min / Max', '{:d} / {:d}'.format(Min, Max)])
    infos.append(['Median', '{:d}'.format(median)])
    infos.append(['Mean / StdDev', '{:.2f} / {:.2f}'.format(mean, stdev)])

    title = 'Image information '
    label = '<h4>' + self.imName + '</h4>'
    spqd.ShowImageInfo(title, label, infos).run()

  #
  #  H E L P   M E N U
  #
  def fn_help(self):
    spqd.HelpDialog().run()

  def fn_about(self):
    title = '<h2><center>' + 'smilPyQtGui - v0.1' + '</center></h2>'

    message = [
      'PyQt Graphical Interface for Smil Library', '<p>',
      'CMM - Centre de Morphologie Mathematique', '<p>',
      'Jose-Marcio Martins da Cruz', '<p>',
      'Jose-Marcio.Martins@minesparis.psl.eu', '<p>',
      'https://github.com/MinesParis-MorphoMath/'
    ]
    message = [
      'PyQt Graphical Interface for Smil Library', '',
      'CMM - Centre de Morphologie Mathematique', '',
      'Jose-Marcio Martins da Cruz', 'Jose-Marcio.Martins@minesparis.psl.eu',
      '', 'https://github.com/MinesParis-MorphoMath/'
    ]
    #spqd.ShowMessage(title, '\n'.join(message), mStyle='center')
    spqd.ShowInfoDialog(title, message, Qt.AlignCenter)

  def fn_aboutqt(self):
    smGui.app.aboutQt()

  #
  #
  #
  def updateFromLinker(self, point=None, sliderValue=None, zoom=None):
    #
    if not point is None:
      pass
    #
    if not sliderValue is None:
      self.slider.setSliderPosition(sliderValue)
      self.curSlice = sliderValue
      self.update(sliderChanged=True)
    #
    if not zoom is None:
      pass

  #
  #
  #
  def sliderValueChanged(self, arg):
    if debug:
      print('Slider - new value : {:d}'.format(arg))
    self.curSlice = arg
    self.update(sliderChanged=True)
    for k in self.linkedImages.keys():
      view = self.linkedImages[k]
      uuid = view.uuid
      if not smGui.isRegistered(uuid):
        del self.linkedImages[k]
      view.updateSliderFromOther(arg)

  def closeEvent(self, event):
    smGui.unregister(self.uuid)
    event.accept()

  def printImage(self):
    """Print image and use QPrinter to select the
    native system format for the printer dialog."""
    printer = QPrinter()
    # Configure the printer
    print_dialog = QPrintDialog(printer)
    if print_dialog.exec() == QDialog.DialogCode.Accepted:
      # Use QPainter to output a PDF file
      painter = QPainter()
      painter.begin(printer)
      # Create QRect object to hold the painter's current
      # viewport, which is the image_label
      rect = QRect(painter.viewport())
      # Get the size of image_label and use it to set the size
      # of the viewport
      pixmap = self.smScene.qPixmap
      size = QSize(pixmap.size())
      size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
      painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
      painter.setWindow(pixmap.rect())
      # Scale the image_label to fit the rect source (0, 0)
      painter.drawPixmap(0, 0, pixmap)
      painter.end()

  def saveImage(self):
    """Display QFileDialog to select image location and
      save the image."""
    image_file, _ = QFileDialog.getSaveFileName(
      self, "Save Image", "", "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;\
              Bitmap Files (*.bmp);;GIF Files (*.gif)")

    pixmap = self.smScene.qPixmap
    if image_file and pixmap.isNull() == False:
      pixmap.save(image_file)
    else:
      QMessageBox.information(self, "Not Saved", "Image not saved.",
                              QMessageBox.StandardButton.Ok)


# =============================================================================
#
#  #    #    ##       #    #    #
#  ##  ##   #  #      #    ##   #
#  # ## #  #    #     #    # #  #
#  #    #  ######     #    #  # #
#  #    #  #    #     #    #   ##
#  #    #  #    #     #    #    #
#
# -----------------------------------------------------------------------------
#
#


# =============================================================================
#
#
def main(args=None):

  print("Not yet...")


if __name__ == '__main__':
  import sys

  sys.exit(main(sys.argv))
