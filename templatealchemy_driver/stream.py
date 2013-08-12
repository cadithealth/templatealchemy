# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.stream
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/05
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

'''
A TemplateAlchemy source that gets the template source from a
file-like object. Note that the file is by default buffered into
memory (so that it can be served multiple times) -- see the
`replayable` constructor parameter (but be aware that setting this to
False could break applications that depend on loading the same
template multiple times with different parameters for discovery
purposes).
'''

# todo: really, any system that expects to be able to call a template
#       multiple times should do the buffering itself... perhaps
#       provide a helper routine to make this easier somehow?...

from StringIO import StringIO
from templatealchemy import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return StreamSource(spec)

#------------------------------------------------------------------------------
class StreamSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec, replayable=True, *args, **kw):
    super(StreamSource, self).__init__(repr(spec), *args, **kw)
    self.stream  = spec
    self._buffer = replayable

  #----------------------------------------------------------------------------
  def getSource(self, name):
    return self

  #----------------------------------------------------------------------------
  def getFormats(self):
    return ['data']

  #----------------------------------------------------------------------------
  def get(self, format):
    if self._buffer is False:
      return self.stream
    if self._buffer is None or self._buffer is True:
      self._buffer = self.stream.read()
    return StringIO(self._buffer)

  #----------------------------------------------------------------------------
  def getRelated(self, name):
    return None

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
