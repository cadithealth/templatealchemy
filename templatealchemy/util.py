# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.util
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

# todo: replace with aadict, asset, morph

import inspect, sys
PY3 = sys.version_info[0] == 3

#------------------------------------------------------------------------------
def resolve(spec):
  spec = spec.split('.')
  used = spec.pop(0)
  found = __import__(used)
  for cur in spec:
    used += '.' + cur
    try:
      found = getattr(found, cur)
    except AttributeError:
      __import__(used)
      found = getattr(found, cur)
  return found

#------------------------------------------------------------------------------
class adict(dict):
  def __getattr__(self, key):
    return self.get(key, None)
  def __setattr__(self, key, value):
    self[key] = value
    return self
  def __delattr__(self, key):
    if key in self:
      del self[key]
    return self
  def update(self, *args, **kw):
    args = [e for e in args if e]
    dict.update(self, *args, **kw)
    return self
  @staticmethod
  def __dict2adict__(subject, recursive=False):
    if isinstance(subject, list):
      if not recursive:
        return subject
      return [adict.__dict2adict__(val, True) for val in subject]
    if not isinstance(subject, dict):
      return subject
    ret = adict(subject)
    if not recursive:
      return ret
    for key, val in ret.items():
      ret[key] = adict.__dict2adict__(val, True)
    return ret

#------------------------------------------------------------------------------
def callingPkgName(ignore=None):
  if ignore is None:
    ignore = []
  elif isinstance(ignore, basestring):
    ignore = [ignore]
  else:
    ignore = ignore[:]
  ignore.append('templatealchemy')
  ignore.append('ta')

  stack = inspect.stack()
  record = None
  try:
    for record in stack:
      if not record or not record[0]:
        continue
      mod = inspect.getmodule(record[0])
      if not mod:
        continue
      mod = getattr(mod, '__package__', None)
      if mod not in ignore:
        return mod
    return None
  finally:
    del record
    del stack

#------------------------------------------------------------------------------
if PY3:
  def isstr(obj):
    return isinstance(obj, str)
else:
  def isstr(obj):
    return isinstance(obj, basestring)

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
