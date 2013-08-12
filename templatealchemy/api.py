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
class Driver(object):

  #----------------------------------------------------------------------------
  def __init__(self, spec=None, *args, **kw):
    super(Driver, self).__init__(*args, **kw)
    self.spec = spec

  #----------------------------------------------------------------------------
  @property
  def uri(self):
    ret = self.__class__.__module__.split('.')
    ret = '.'.join(ret[1 if ret[0] == 'templatealchemy_driver' else 0:])
    return ':'.join(filter(None, [ret, self.spec]))

  #----------------------------------------------------------------------------
  def resolveUri(self, uri, base=None):
    return os.path.normpath(
      os.path.join(os.path.dirname(base or self.uri), uri))

#------------------------------------------------------------------------------
class Source(Driver):

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

#------------------------------------------------------------------------------
class Renderer(Driver):

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

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
