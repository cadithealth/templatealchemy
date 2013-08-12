# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.mako
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from __future__ import absolute_import

import mako.template, yaml
from mako.lookup import TemplateLookup
from templatealchemy import api, util, engine

#------------------------------------------------------------------------------
def loadRenderer(spec=None):
  return MakoRenderer(spec)

#------------------------------------------------------------------------------
class TaLookup(TemplateLookup):
  # TODO: this is not very efficient in the case that building a source
  #       is expensive...
  def __init__(self, source, renderer):
    self.source   = source
    self.renderer = renderer
  def adjust_uri(self, uri, relativeto):
    return self.source.resolveUri(uri, relativeto)
  def get_template(self, uri):
    src = engine.loadSource(uri)
    return self.ta_template(text=src.get('').read(), uri=uri)
  def ta_template(self, **kw):
    kw['lookup'] = self
    kw.update(self.renderer.params)
    return mako.template.Template(**kw)

#------------------------------------------------------------------------------
class MakoRenderer(api.Renderer):

  #----------------------------------------------------------------------------
  def __init__(self, *args, **kw):
    super(MakoRenderer, self).__init__(*args, **kw)
    self.params = yaml.load(self.spec or '{default_filters: ["h"]}')

  #----------------------------------------------------------------------------
  def render(self, context, stream, params):
    if context.makoLookup is None:
      context.makoLookup = TaLookup(context.template.source, self)
    return context.makoLookup.ta_template(
      text = stream.read(),
      uri  = context.template.source.uri,
      ).render(**params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
