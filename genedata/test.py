# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.test
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest, os.path
import genedata
from genedata.util import adict

#------------------------------------------------------------------------------
class TestGenedata(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_mustache(self):
    root = genedata.Template(
      source='pkg:genedata:test_data/mustache',
      renderer='mustache')
    tpl = root.getTemplate('document')
    out = tpl.render('html', adict(
        title='Genedata',
        doc=adict(title='Mustache'),
        sections=[
          adict(title='Overview', text='Good'),
          adict(title='Details', text='Poor'),
          adict(title='Utility', text='Excellent'),
          ]))
    chk = '''\
<html>
 <head>
  <title>Genedata</title>
 </head>
 <body>
  <h1>Genedata</h1>
  <h2>Mustache</h2>
   <h3>Overview</h3>
   <p>Good</p>
   <h3>Details</h3>
   <p>Poor</p>
   <h3>Utility</h3>
   <p>Excellent</p>
 </body>
</html>
'''
    self.assertMultiLineEqual(out, chk)

  #----------------------------------------------------------------------------
  def test_mako(self):
    root = genedata.Template(
      source='pkg:genedata:test_data/mako',
      renderer='mako')
    tpl = root.getTemplate('document')
    out = tpl.render('html', adict(
        title='Genedata',
        doc=adict(title='Mako'),
        sections=[
          adict(title='Overview', text='Good'),
          adict(title='Details', text='Poor'),
          adict(title='Utility', text='Excellent'),
          ]))
    chk = '''\
<html>
 <head>
  <title>Genedata</title>
 </head>
 <body>
  <h1>Genedata</h1>
  <h2>Mako</h2>
   <h3>Overview</h3>
   <p>Good</p>
   <h3>Details</h3>
   <p>Poor</p>
   <h3>Utility</h3>
   <p>Excellent</p>
 </body>
</html>
'''
    self.assertMultiLineEqual(out, chk)

  #----------------------------------------------------------------------------
  def test_sqlalchemy(self):
    # todo: what if genedata is a zipped archive?...
    path = os.path.join(os.path.dirname(__file__), 'test_data/sa/source.db')
    root = genedata.Template(
      source='sqlalchemy:sqlite:///' + path,
      renderer='mustache')
    tpl = root.getTemplate('document')
    out = tpl.render('html', adict(title='Genedata'))
    chk = '<html><body><h1>Genedata</h1></body></html>'
    self.assertMultiLineEqual(out, chk)

  #----------------------------------------------------------------------------
  def test_string(self):
    root = genedata.Template(source='string:ALL YOUR ${plan["from"]} ARE BELONG TO ${plan["to"]}')
    params = dict(plan=adict((('from', 'BASE'), ('to', 'US'))))
    outt = root.render('text', params)
    outh = root.render('html', params)
    self.assertEqual(outt, 'ALL YOUR BASE ARE BELONG TO US')
    self.assertEqual(outh, 'ALL YOUR BASE ARE BELONG TO US')

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
