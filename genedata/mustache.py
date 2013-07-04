# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.mustache
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import pystache
from genedata import api, util

#------------------------------------------------------------------------------
def loadRenderer(spec=None):
  return MustacheRenderer(spec)

#------------------------------------------------------------------------------
class MustacheRenderer(api.Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, spec):
    self.spec = spec

  #----------------------------------------------------------------------------
  def render(self, context, data, params):
    # todo: do anything with `spec`?
    return pystache.render(data, params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
