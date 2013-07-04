# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.mako
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from __future__ import absolute_import

import mako.template
from genedata import api, util

#------------------------------------------------------------------------------
def loadRenderer(spec=None):
  return MakoRenderer(spec)

#------------------------------------------------------------------------------
class MakoRenderer(api.Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    # TODO: expose control of `mako.template.Template()` args/kwargs...
    self.spec = spec
    self.lookup = None
    self.filters = ['h']

  #----------------------------------------------------------------------------
  def render(self, context, data, params):
    # TODO: take advantage of mako's `TemplateLookup` class...
    tpl = mako.template.Template(
      text=data, lookup=self.lookup, default_filters=self.filters)
    return tpl.render(**params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
