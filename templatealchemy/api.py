# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.api
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os.path

__all__ = ('Source', 'Renderer')

#------------------------------------------------------------------------------
class Source(object):

  #----------------------------------------------------------------------------
  def __init__(self, uri, *args, **kw):
    self.uri = uri

  #----------------------------------------------------------------------------
  def get(self, format):
    '''
    Returns the source content stream for the current template source
    for the specified `format`. The returned object must be a
    file-like object supporting read access.
    '''
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def getSource(self, name):
    '''
    Returns a subsidiary source template, relative to the current
    template, with the specified `name`. This is seen as a hierchical
    relationship, and is typically represented as a slash ('/')
    delimited path.
    '''
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def getFormats(self):
    '''
    Returns a list of all the available formats for this source.
    '''
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    '''
    Returns a content stream for the related object `name` that is
    relative to the current template. Typically this is used for
    meta-information *spec* definitions using the "!include" or
    "!include-raw" directives. As with :meth:`get`, the returned
    object must be a file-like object supporting read access.
    '''
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def ns(self, scheme, spec):
    if not spec:
      return scheme
    return scheme + ':' + spec

  #----------------------------------------------------------------------------
  def resolveUri(self, uri, base=None):
    return os.path.normpath(
      os.path.join(os.path.dirname(base or self.uri), uri))

#------------------------------------------------------------------------------
class Renderer(object):

  #----------------------------------------------------------------------------
  def __init__(self, uri, *args, **kw):
    self.uri = uri

  #----------------------------------------------------------------------------
  def render(self, context, stream, params):
    '''
    Renders the given template data `stream` (as a read-access
    file-like object) to serialized rendered output. The given
    `params` provide variables that are typically passed to the
    template using template-specific mechanisms.

    todo: update this when the time comes:

    `context` is a reserved parameter that is intended to enable
    cross-driver optimizations, but has not been defined at this
    point.
    '''
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def ns(self, scheme, spec):
    if not spec:
      return scheme
    return scheme + ':' + spec

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
