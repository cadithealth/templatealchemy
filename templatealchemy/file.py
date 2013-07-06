# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.file
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

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
  def get(self, format):
    with open(self.path + '.' + format, 'rb') as fp:
      return fp.read()

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
