# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.string
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
  def getSource(self, name):
    return self

  #----------------------------------------------------------------------------
  def getFormats(self):
    return ['data']

  #----------------------------------------------------------------------------
  def get(self, format):
    return StringIO(self.spec)

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    return None

  #----------------------------------------------------------------------------
  def resolveUri(self, uri, base=None):
    if uri.startswith('pkg:'):
      return uri
    # forcing all "string:" to use "pkg" sources...
    # todo: perhaps inspect `uri` to see if it is resolvable as-is?...
    return 'pkg:' + uri

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
