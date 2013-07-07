# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.mustache
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
  def __init__(self, spec):
    self.spec = spec

  #----------------------------------------------------------------------------
  def render(self, context, stream, params):
    # todo: do anything with `spec`?
    return pystache.render(stream.read(), params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
