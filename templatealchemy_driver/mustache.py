# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.mustache
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

  # todo: any customizations to load from `self.spec`?...

  #----------------------------------------------------------------------------
  def render(self, context, stream, params):
    return pystache.render(stream.read(), params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
