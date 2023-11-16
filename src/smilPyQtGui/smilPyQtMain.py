#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  smilPyQtMain.py
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

import sys

from smilPyQtView import smilQtView
from PyQt5.QtWidgets import QApplication
from smilPyQtDlog import ViewManagerDialog


# =============================================================================
#
#
class smilGui:
  last = 0
  views = {}

  def __init__(self, argv=[]):
    self.app = QApplication(argv)

  def imView(self, img=None):
    """ Create a view window for an image
    """
    if img is None:
      return None

    self.last += 1
    uuid = str(self.last)
    view = smilQtView(img, uuid=uuid)
    view.parent = self
    self.views[uuid] = view

    return view

  #
  def _setVis(self, view, visible):
    if visible:
      view.show()
    else:
      view.hide()

  def imSetVisible(self, img=None, visible=True):
    """Set the visible state of the image window

    Parameters
    ----------
    img :
      The image variable or the identifier (str or int)
    visible:
      The new state to be set (True if visible and False to hide)
    """

    if isinstance(img, (str, int)):
      k = str(img)
      if k in self.views.keys():
        self._setVis(self.views[k], visible)
        return

    for k in self.views.keys():
      if id(self.views[k].image) == id(img):
        self._setVis(self.views[k], visible)
        break

  def imSetVisibleAll(self, visible=True):
    """Set the visible state of all image windows

    Parameters
    ----------
    visible:
      The new state to be set (True if visible and False to hide)
    """
    for k in self.views.keys():
      self.setVis(self.views[k], visible)

  #
  def imHide(self, img=None):
    if isinstance(img, (str, int)):
      k = str(img)
      if k in self.views.keys():
        self.views[k].hide()
      return
    for k in self.views.keys():
      if id(self.views[k].image) == id(img):
        self.views[k].hide()
        break

  def imHideAll(self):
    for k in self.views.keys():
      self.views[k].hide()

  #
  def imClose(self, img=None):
    if isinstance(img, (str, int)):
      k = str(img)
      if k in self.views.keys():
        self.views[k].close()
      if k in self.views.keys():
        del self.views[k]
      return
    for k in self.views.keys():
      if id(self.views[k].image) == id(img):
        self.views[k].close()
        if k in self.views.keys():
          del self.views[k]
        break

  def imCloseAll(self):
    for k in self.views.keys():
      self.views[k].close()
      if k in self.views.keys():
        del self.views[k]

  def getCopy(self):
    res = {}
    for k in self.views.keys():
      res[k] = self.views[k]
    return res

  def unregister(self, uuid=None):
    if uuid in self.views.keys():
      del self.views[uuid]

  def isRegistered(self, uuid):
    return uuid in self.views.keys()

  def viewManager(self):
    dTmp = {}
    dAll = self.views
    for k in dAll.keys():
      dTmp[k] = dAll[k]
    wdlog = ViewManagerDialog(dTmp).run()

  def listViews(self):
    for k in self.views.keys():
      print("{:>5} - {:}".format(k, self.views[k].imName))


# =============================================================================
#
#
def main(args=None):
  return 0


# =============================================================================
#
#
if __name__ == '__main__':

  sys.exit(main(sys.argv))
