# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.string
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return StringSource(spec)

#------------------------------------------------------------------------------
class StringSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    self.data = spec

  #----------------------------------------------------------------------------
  def getSource(self, name):
    raise SyntaxError('`string` sources do not support sub-sources')

  #----------------------------------------------------------------------------
  def get(self, format):
    return self.data

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
