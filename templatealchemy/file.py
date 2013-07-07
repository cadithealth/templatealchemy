# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.file
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return FileSource(spec)

#------------------------------------------------------------------------------
class FileSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    self.path = spec

  #----------------------------------------------------------------------------
  def getSource(self, name):
    return FileSource(self.path + '/' + name)

  #----------------------------------------------------------------------------
  def getFormats(self):
    path, base = os.path.split(self.path)
    base += '.'
    return [
      cur[len(base):]
      for cur in os.listdir(path)
      if cur.startswith(base) and os.path.isfile(os.path.join(path, cur))]

  #----------------------------------------------------------------------------
  def get(self, format):
    # todo: what about file descriptor clean-up?...
    return open(self.path + '.' + format, 'rb')

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    if name.startswith('/'):
      return open(name, 'rb')
    return open(os.path.dirname(self.path) + '/' + name, 'rb')

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
