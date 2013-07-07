# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.stream
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/05
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

'''
A TemplateAlchemy source that gets the template source from a
file-like object. Note that the file is not buffered, and therefore
the template is "single-use".
'''

from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return StreamSource(spec)

#------------------------------------------------------------------------------
class StreamSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    self.stream = spec

  #----------------------------------------------------------------------------
  def getSource(self, name):
    raise SyntaxError('`stream` sources do not support sub-sources')

  #----------------------------------------------------------------------------
  def getFormats(self):
    return []

  #----------------------------------------------------------------------------
  def get(self, format):
    return self.stream

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    return None

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
