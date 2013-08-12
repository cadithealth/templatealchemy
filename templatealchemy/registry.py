# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/30
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import yaml
from .engine import Manager
from .util import resolve

__all__ = ('Registry',)

#------------------------------------------------------------------------------
class Registry(object):

  #----------------------------------------------------------------------------
  def __init__(self, settings=None, prefix=None):
    self.managers = dict()
    self.default  = None
    self.configure(settings, prefix)

  #----------------------------------------------------------------------------
  def configure(self, settings=None, prefix=None, clear=False):
    if clear:
      self.managers = dict()
    if settings is None:
      return
    configs = dict()
    prefix  = prefix or ''
    regpfx  = prefix + 'registry.'
    for key in settings.keys():
      if not key.startswith(regpfx):
        continue
      name = key[len(regpfx):].split('.', 1)[0]
      if name not in configs:
        configs[name] = dict()
      param = key[len(regpfx) + len(name) + 1:]
      if param == 'extmap':
        configs[name][param] = yaml.load(settings.get(key))
      elif param == 'fmtcmp':
        configs[name][param] = resolve(settings.get(key))
      else:
        configs[name][param] = settings.get(key)
    for name, params in configs.items():
      self.managers[name] = Manager(
        source   = params.get('source'),
        renderer = params.get('renderer'),
        extmap   = params.get('extmap'),
        fmtcmp   = params.get('fmtcmp'),
        )
    self.default = self.managers.get(
      settings.get(prefix + 'default', 'default'), None)

  #----------------------------------------------------------------------------
  def get(self, name):
    return self.managers.get(name, self.default)

  #----------------------------------------------------------------------------
  def set(self, name, manager):
    self.managers[name] = manager
    return self

  #----------------------------------------------------------------------------
  def __getitem__(self, name):
    return self.get(name)

  #----------------------------------------------------------------------------
  def __setitem__(self, name, manager):
    return self.set(name, manager)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
