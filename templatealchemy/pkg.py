# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.pkg
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import pkgutil
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return PkgSource(spec)

#------------------------------------------------------------------------------
class PkgSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    self.module, self.path = spec.split(':', 1)

  #----------------------------------------------------------------------------
  def getSource(self, name):
    return PkgSource(self.module + ':' + self.path + '/' + name)

  #----------------------------------------------------------------------------
  def get(self, format):
    return pkgutil.get_data(self.module, self.path + '.' + format)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
