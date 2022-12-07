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

import os
import sys

#import glob
#import psutil

#import fnmatch as fn
import re
import datetime

import math as m
import numpy as np


import smilPython as sp

from smilPyQtView import *
from smilPyQtDlog import *

# =============================================================================
#
#
class smilGui:
  last = 0
  views = {}

  def __init__(self, argv=[]):
    self.app = QApplication(argv)

  def imShow(self, img = None):
    if img is None:
      return None

    self.last += 1
    uuid = str(self.last)
    view = smilQtView(img, uuid = uuid)
    view.parent = self
    self.views[uuid] = view

    return view

  def imHide(self, img = None):
    if isinstance(img, (str, int)):
      k = str(img)
      if k in self.views.keys():
        self.views[k].hide()
    for k in self.views.keys():
      if id(self.views[k].image) == id(img):
        self.views[k].hide()
        break

  def imHideAll(self):
    for k in self.views.keys():
      self.views[k].hide()

  def imClose(self, img = None):
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

  def unregister(self, uuid = None):
    if uuid in self.views.keys():
      del self.views[uuid]

  def isRegistered(self, uuid):
    return uuid in self.views.keys()

  def viewManager(self):
    dTmp = {}
    dAll = self.views
    for k in dAll.keys():
      dTmp[k] = dAll[k]
    w = ViewManagerDialog(dTmp).run()

  def listViews(self):
    for k in self.views.keys():
      print("{:>5} - {:}".format(k, self.views[k].imName))

# =============================================================================
#
#
def dummy(cli):
  return 0

# =============================================================================
#
#
def main(args=None):
  return 0

# =============================================================================
#
#
if __name__ == '__main__':
  import sys


  sys.exit(main(sys.argv))
