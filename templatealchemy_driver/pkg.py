# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.pkg
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import pkgutil, pkg_resources, os.path, six
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return PkgSource(spec)

#------------------------------------------------------------------------------
class PkgSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(PkgSource, self).__init__(*args, **kw)
    self.module, self.path = self.spec.split(':', 1)

  #----------------------------------------------------------------------------
  def getSource(self, name):
    if name is None:
      return self
    return PkgSource(self.spec + '/' + name)

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
    if format:
      format = '.' + format
    return six.StringIO(pkgutil.get_data(self.module, self.path + format))

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    if name.startswith('/'):
      name = name[1:]
    else:
      name = os.path.dirname(self.path) + '/' + name
    return six.StringIO(pkgutil.get_data(self.module, name))

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
