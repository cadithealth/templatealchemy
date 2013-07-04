# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.api
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
class Source(object):

  #----------------------------------------------------------------------------
  def get(self, spec):
    raise NotImplementedError()

  #----------------------------------------------------------------------------
  def getSource(self, name):
    raise NotImplementedError()

#------------------------------------------------------------------------------
class Renderer(object):

  #----------------------------------------------------------------------------
  def render(self, context, data, params):
    raise NotImplementedError()

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
