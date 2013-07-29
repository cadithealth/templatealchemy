# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.driver.mustache
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import pystache
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadRenderer(spec=None):
  return MustacheRenderer(spec)

#------------------------------------------------------------------------------
class MustacheRenderer(api.Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, spec, *args, **kw):
    super(MustacheRenderer, self).__init__(self.ns('mustache', spec), *args, **kw)
    self.spec = spec

  #----------------------------------------------------------------------------
  def render(self, context, stream, params):
    # todo: do anything with `self.spec`?
    return pystache.render(stream.read(), params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
