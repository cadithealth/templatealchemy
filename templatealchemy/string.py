# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.string
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from StringIO import StringIO
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return StringSource(spec)

#------------------------------------------------------------------------------
class StringSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec, *args, **kw):
    super(StringSource, self).__init__(self.ns('string', spec), *args, **kw)
    self.data = spec

  #----------------------------------------------------------------------------
  def getSource(self, name):
    return self

  #----------------------------------------------------------------------------
  def getFormats(self):
    return ['data']

  #----------------------------------------------------------------------------
  def get(self, format):
    return StringIO(self.data)

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    return None

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
