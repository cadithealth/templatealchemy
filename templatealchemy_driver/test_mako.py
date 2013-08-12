# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy_driver.test_mako
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/08/12
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest, os.path
import templatealchemy
from templatealchemy.util import adict

#------------------------------------------------------------------------------
class TestMakoDriver(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_mako(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mako',
      renderer='mako',
      extmap={'text': 'txt'})
    tpl = root.getTemplate('document')
    params = adict(
      title='TemplateAlchemy',
      doc=adict(title='Mako'),
      sections=[
        adict(title='Overview', text='Good'),
        adict(title='Details', text='Poor'),
        adict(title='Utility', text='Excellent'),
        ])
    out = tpl.render('html', params)
    chk = '''\
<html>
 <head>
  <title>TemplateAlchemy</title>
 </head>
 <body>
  <h1>TemplateAlchemy</h1>
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
    out = tpl.render('text', params)
    chk = '''\
# TemplateAlchemy

## Mako

### Overview

Good

### Details

Poor

### Utility

Excellent
'''
    self.assertMultiLineEqual(out, chk)
    self.assertEqual(tpl.meta.formats, ['html', 'text'])

  #----------------------------------------------------------------------------
  def test_mako_defaultFilters(self):
    src = 'string:<div>${content}</div>'
    tpl = templatealchemy.Template(source=src, renderer='mako')
    self.assertEqual(tpl.render('html',dict(content='<h1>Title</h1>')),
                     '<div>&lt;h1&gt;Title&lt;/h1&gt;</div>')
    tplnoh = templatealchemy.Template(source=src, renderer='mako:{default_filters: null}')
    self.assertEqual(tplnoh.render('html',dict(content='<h1>Title</h1>')),
                     '<div><h1>Title</h1></div>')

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
