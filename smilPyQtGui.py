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
# This script does...
#
# History : xx/xx/xxxx - Jose-Marcio Martins da Cruz
#           Just created
#

from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout

from PyQt5.QtWidgets import (QLabel, QSizePolicy, QScrollArea, QMessageBox,
                             QMainWindow, QMenu, QAction, qApp, QFileDialog,
                             QInputDialog, QStatusBar, QTextEdit, QWidget,
                             QDialog, QGraphicsView, QGraphicsScene, QSlider,
                             QLineEdit)

from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QIcon, QColor, qRgb

from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from smilPyQtDlog import *

# =============================================================================
#

class SmilGui:
  last = 0
  views = {}

  def __init__(self, argv=[]):
    self.app = QApplication(argv)
    #self.views = {}

  def nextUuid():
    SmilGui.last += 1
    uuid = '{:d}'.format(SmilGui.last)
    return uuid

  def register(self, view):
    uuid = SmilGui.nextUuid()
    SmilGui.views[uuid] = view
    return uuid

  def _getViewByImage(self, image):
    for uuid in SmilGui.views.keys():
      if SmilGui.views[uuid] == image:
        return uuid
    return None

  def unregister(self, key=None):
    if key is None:
      return

    if not isinstance(key, str):
      uuid = _getViewByImage(key)
    else:
      uuid = key

    if uuid in SmilGui.views.keys():
      del SmilGui.views[uuid]

  def isRegistered(self, uuid):
    return uuid in SmilGui.views.keys()

  def getCopy(self):
    res = {}
    for k in SmilGui.views.keys():
      res[k] = SmilGui.views[k]
    return res

  def hideView(self, uuid=None):
    if uuid in SmilGui.views.keys():
      SmilGui.views[uuid].hide()

  def hideAll(self):
    for uuid in self.views.keys():
      self.hideView(uuid)

  def showView(self, uuid=None):
    if uuid in SmilGui.views.keys():
      SmilGui.views[uuid].show()

  def showAll(self):
    for uuid in SmilGui.views.keys():
      self.showView(uuid)

  def viewManager(self):
    dTmp = {}
    dAll = SmilGui.views
    for k in dAll.keys():
      dTmp[k] = dAll[k]
    w = ViewManagerDialog(dTmp).run()

  def listViews(self):
    for k in SmilGui.views.keys():
      print("{:} {:}".format(k, SmilGui.views[k]))

    pass


gSmilGui = SmilGui()


# =============================================================================
#
if __name__ == '__main__':

  print(SmilGui.last)
  print(gSmilGui.last)
  w = QDialog()
  w.imName = "1"
  gSmilGui.addView(w)
  print(gSmilGui.last)

  w = QDialog()
  w.imName = "2"
  gSmilGui.addView(w)
  print(gSmilGui.last)

  gSmilGui.listViews()
  gSmilGui.viewManager()
