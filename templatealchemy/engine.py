# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.engine
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from . import util

__all__ = ['Template', 'loadSource', 'loadRenderer']

#------------------------------------------------------------------------------
def loadSource(spec):
  # TODO: make this do more error detection and reporting...
  if spec is None:
    spec = 'pkg'
  if not isinstance(spec, basestring):
    return spec
  spec = spec.split(':', 1)
  loader = util.resolve('templatealchemy.' + spec.pop(0) + '.loadSource')
  return loader(spec.pop(0) if spec else None)

#------------------------------------------------------------------------------
def loadRenderer(spec):
  # TODO: make this do more error detection and reporting...
  if spec is None:
    spec = 'mako'
  if not isinstance(spec, basestring):
    return spec
  spec = spec.split(':', 1)
  loader = util.resolve('templatealchemy.' + spec.pop(0) + '.loadRenderer')
  return loader(spec.pop(0) if spec else None)

#------------------------------------------------------------------------------
class Template(object):

  #----------------------------------------------------------------------------
  def __init__(self, source=None, renderer=None):
    # TODO: if `source` is None default to caller's package...
    self.source   = loadSource(source)
    self.renderer = loadRenderer(renderer)

  #----------------------------------------------------------------------------
  def getTemplate(self, name):
    return Template(self.source.getSource(name), self.renderer)

  #----------------------------------------------------------------------------
  def render(self, format, params):
    return self.renderer.render(None, self.source.get(format), params)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
