# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.engine
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os, yaml
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
def makeLoader(source, relativeTo=None):
  class SourceLoader(yaml.Loader):
    def _include(self, node):
      path = os.path.join(relativeTo or '', node.value)
      return yaml.load(source.getRelated(path).read(),
                       Loader=makeLoader(source, os.path.dirname(path)))
    def _includeRaw(self, node):
      path = os.path.join(relativeTo or '', node.value)
      return source.getRelated(path).read()
  SourceLoader.add_constructor('!include', SourceLoader._include)
  SourceLoader.add_constructor('!include-raw', SourceLoader._includeRaw)
  return SourceLoader

#------------------------------------------------------------------------------
class Template(object):

  # TODO: implement template caching?...

  #----------------------------------------------------------------------------
  def __init__(self, source=None, renderer=None, extmap=None):
    '''
    Construct a new top-level Template with the given `source` and
    `renderer`.

    :Parameters:

    source : { str, templatealchemy.api.Source }

      The persistent read-access storage of template source
      content. The `source` must either be a subclass of
      :class:`templatealchemy.api.Source` or a source specification
      string in the format ``TYPE[:SPEC]``.

    renderer : { str, templatealchemy.api.Renderer }

      The rendering engine for this template. The `renderer` must
      either be a subclass of :class:`templatealchemy.api.Renderer` or
      a renderer specification string in the format ``TYPE[:SPEC]``.

    extmap : dict, optional

      The `extmap` parameter allows remapping of format to extension,
      where needed. For example, if "html" formats for a given
      template are stored on the filesystem with the extension "mako",
      but "text" formats are stored with the extension "mako.txt",
      then the following extmap could be used::

        extmap = { 'html': 'mako', 'text': 'mako.txt' }

      and on the filesystem, for the template
      'pkg:demo:templates/document' you might have the following file
      structure::

        -- demo/templates/
           |-- document.mako
           `-- document.mako.txt

      Note that the special format ``None`` (the symbol, not the
      string) can be used in this dictionary to refer to the default
      template. Generally speaking, it is acceptable to map *to* None,
      but not *from* None to some other value -- the latter is
      typically left to the source itself.
    '''
    # TODO: if `source` is None default to caller's package...
    self.source   = loadSource(source)
    self.renderer = loadRenderer(renderer)
    self._meta    = None
    self.extmap   = extmap or dict()
    self.rextmap  = {val: key for key, val in self.extmap.items()}

  #----------------------------------------------------------------------------
  def getTemplate(self, name):
    return Template(self.source.getSource(name), self.renderer,
                    extmap=self.extmap)

  #----------------------------------------------------------------------------
  def render(self, format, params):
    if format == 'spec':
      raise TypeError('format "spec" is reserved for internal TemplateAlchemy use')
    format = self.extmap.get(format, format)
    return self.renderer.render(None, self.source.get(format), params)

  #----------------------------------------------------------------------------
  @property
  def meta(self):
    if self._meta is not None:
      return self._meta
    formats = sorted(self.source.getFormats())
    if 'spec' in formats:
      self._meta = yaml.load(self.source.get('spec'), makeLoader(self.source))
      self._meta = util.adict.__dict2adict__(self._meta, recursive=True)
    else:
      self._meta = util.adict()
    self._meta.formats = [self.rextmap.get(fmt, fmt)
                          for fmt in formats if fmt != 'spec']
    return self._meta

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
