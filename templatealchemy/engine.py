# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.engine
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import os, yaml, re
from . import util, api
from .util import adict, isstr

__all__ = ('Manager', 'Template', 'loadSource', 'loadRenderer')

#------------------------------------------------------------------------------
def loadSource(spec):
  # TODO: make this do more error detection and reporting...
  if spec is None:
    spec = 'pkg'
  if not isinstance(spec, basestring):
    return spec
  spec = spec.split(':', 1)
  loader = util.resolve('templatealchemy_driver.' + spec.pop(0) + '.loadSource')
  return loader(spec.pop(0) if spec else None)

#------------------------------------------------------------------------------
def loadRenderer(spec):
  # TODO: make this do more error detection and reporting...
  if spec is None:
    spec = 'mako'
  if not isinstance(spec, basestring):
    return spec
  spec = spec.split(':', 1)
  loader = util.resolve('templatealchemy_driver.' + spec.pop(0) + '.loadRenderer')
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
  def __init__(self, source=None, renderer=None, extmap=None, fmtcmp=None):
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
      but not *from* None to some other value.

      Note also that it is best to keep this mapping a one-to-one
      relationship, but it is nonetheless possible to map multiple
      declared extensions to the same filesystem extension. For
      example, both formats 'html' and 'text' could map to extension
      'mako' -- the same template would then be used to render both
      formats.

    fmtcmp : callable, optional

      Specify the format sorting comparison function, as passed into
      the `cmp` parameter of the `sorted` function. The primary
      consequence of this sorting is that the first format becomes the
      default format. Application-specific logic is required to
      provide a good default format. By default, the formats are
      simply sorted alphabetically.

      @TODO: add smarter default sorting; something like formatted, then
      structured, then semi-structured, then unstructured, then raw::

        xml > xhtml > html > rst > yaml > json > ... > text > data

    '''
    self.source   = loadSource(source)
    self.renderer = loadRenderer(renderer)
    self.context  = adict(template=self)
    self._meta    = None
    self.extmap   = extmap or dict()
    self.rextmap  = dict()
    for key, val in self.extmap.items():
      if val not in self.rextmap:
        self.rextmap[val] = []
      self.rextmap[val].append(key)
    # TODO: provide a better default sorter -- see pydocs
    self.fmtcmp   = None

  #----------------------------------------------------------------------------
  def getTemplate(self, source):
    '''
    Loads the sub-template `source` within the context of the current
    template and/or manager.  If `source` is a
    :class:`templatealchemy.api.Source`, then it is used as the source
    for the returned template.  Otherwise, `source` is assumed to be a
    string, and the sub-template is hierarchically loaded from the
    current source.

    '''
    if not isinstance(source, api.Source):
      source = self.source.getSource(source)
    # TODO: i need to move to a `Manager` type of approach so that
    #       i only need to pass one parameter to sub-templates.
    return Template(source, self.renderer,
                    extmap=self.extmap, fmtcmp=self.fmtcmp)

  #----------------------------------------------------------------------------
  def __getitem__(self, name):
    return self.getTemplate(name)

  #----------------------------------------------------------------------------
  def render(self, format, params=None):
    if format == 'spec':
      raise TypeError('format "spec" is reserved for internal TemplateAlchemy use')
    format = self.extmap.get(format, format)
    if not format:
      format = self.meta.formats[0]
    return self.renderer.render(self.context, self.source.get(format),
                                params or dict())

  #----------------------------------------------------------------------------
  @property
  def meta(self):
    if self._meta is not None:
      return self._meta
    formats = sorted(self.source.getFormats(), cmp=self.fmtcmp)
    if 'spec' in formats:
      self._meta = yaml.load(self.source.get('spec'), makeLoader(self.source))
      self._meta = adict.__dict2adict__(self._meta, recursive=True)
    else:
      raw = self.source.get(formats[0]).read()
      if '-*- spec -*-' in raw:
        # TODO: generalize how the spec is defined... perhaps let the
        #       active renderer do so?...
        spec = re.search(r'-\*- spec -\*-(.*?)-\*- /spec -\*-', raw, flags=re.DOTALL)
        if spec:
          self._meta = yaml.load(spec.group(1).strip(), makeLoader(self.source))
          self._meta = adict.__dict2adict__(self._meta, recursive=True)
    if self._meta is None:
      self._meta = adict()
    self._meta.formats = [rfmt
                          for fmt in formats if fmt != 'spec'
                          for rfmt in self.rextmap.get(fmt, [fmt])]
    return self._meta

#------------------------------------------------------------------------------
# TODO: the `Template` class behaves like a manager, so aliasing them... this
#       is probably not "right", but will do for now. eventually, this should
#       be corrected.
Manager = Template

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
