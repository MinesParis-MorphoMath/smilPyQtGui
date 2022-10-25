#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  smilPyQtTools.py
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

images = {}


class WRegister:
  def __init__(self):
    self.reg = {}
    self.last = 0

  def register(self, view=None):
    if view is None:
      return
    self.last += 1
    uuid = "{:s}".format(str(self.last))
    #uuid = uuid.uuid4()
    self.reg[uuid] = view
    return uuid

  def unregister(self, uuid=None):
    if uuid is None:
      return
    if uuid in self.reg.keys():
      del self.reg[uuid]
    else:
      #print("uuid not in list")
      pass

  def print(self):
    print()
    if len(self.reg.keys()) > 0:
      print()
      for k in self.reg.keys():
        print(' {:>5s} {:s}'.format(k, self.reg[k].imName))
      print('-' * 46)
      print(' {:5d} windows registered'.format(len(self.reg.keys())))
    else:
      print('    No windows registered')

  def list(self):
    self.print()

  def showAll(self):
    for k in self.reg.keys():
      self.reg[k].show()

  def hideAll(self):
    for k in self.reg.keys():
      self.reg[k].hide()

  def show(self, uuid):
    pass

  def hide(self, uuid):
    pass


SRegister = WRegister()
