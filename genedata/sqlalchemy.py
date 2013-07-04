# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.sqlalchemy
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

from __future__ import absolute_import

import sqlalchemy as sa
from genedata import api, util

#------------------------------------------------------------------------------
def loadSource(spec=None):
  return SaSource(spec)

#------------------------------------------------------------------------------
class SaSource(api.Source):

  #----------------------------------------------------------------------------
  def __init__(self, spec, name='', tablename=None,
               engine=None, connection=None, table=None, metadata=None
               ):
    self.spec = spec
    self.name = name
    self.engine   = engine or sa.create_engine(spec)
    self.conn     = connection or self.engine.connect()
    self.metadata = metadata or sa.MetaData()
    self.table    = table
    if self.table is None:
      self.table = sa.Table(
        tablename or 'template', self.metadata,
        sa.Column('name', sa.String()),
        sa.Column('format', sa.String()),
        sa.Column('content', sa.LargeBinary()),
        )

  #----------------------------------------------------------------------------
  def getSource(self, name):
    return SaSource(
      self.spec, name=self.name + '/' + name if self.name else name,
      engine=self.engine, metadata=self.metadata, table=self.table,
      connection=self.conn,
      )

  #----------------------------------------------------------------------------
  def get(self, format):
    result = self.conn.execute(
      sa.sql
      .select([self.table.c.content])
      .where(sa.sql.and_(self.table.c.name == self.name,
                         self.table.c.format == format)))
    return result.fetchone()[0]

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
