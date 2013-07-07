# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.pkg
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import pkgutil, pkg_resources, os.path
from StringIO import StringIO
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
  def getFormats(self):
    # todo: is there any way to replicate this pkg_resources functionality
    #       with pkgutil or some other standard library?...
    path, base = os.path.split(self.path)
    base += '.'
    return [
      cur[len(base):]
      for cur in pkg_resources.resource_listdir(self.module, path)
      if cur.startswith(base)
      and not pkg_resources.resource_isdir(
        self.module, os.path.join(path, cur))]

  #----------------------------------------------------------------------------
  def get(self, format):
    return StringIO(pkgutil.get_data(self.module, self.path + '.' + format))

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    if name.startswith('/'):
      name = name[1:]
    else:
      name = os.path.dirname(self.path) + '/' + name
    return StringIO(pkgutil.get_data(self.module, name))

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
