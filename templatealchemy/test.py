# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.test
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import unittest, os.path
import templatealchemy
from templatealchemy.util import adict

#------------------------------------------------------------------------------
class TestTemplateAlchemy(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_mustache(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mustache',
      renderer='mustache')
    tpl = root.getTemplate('document')
    out = tpl.render('html', adict(
        title='TemplateAlchemy',
        doc=adict(title='Mustache'),
        sections=[
          adict(title='Overview', text='Good'),
          adict(title='Details', text='Poor'),
          adict(title='Utility', text='Excellent'),
          ]))
    chk = '''\
<html>
 <head>
  <title>TemplateAlchemy</title>
 </head>
 <body>
  <h1>TemplateAlchemy</h1>
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
    self.assertEqual(tpl.meta.formats, ['html'])

  #----------------------------------------------------------------------------
  def test_extmap(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mustache',
      renderer='mustache',
      extmap={'html': 'mako', 'text': 'mako.txt', 'csv': 'mako.txt'})
    tpl = root.getTemplate('doc2')
    self.assertEqual(tpl.render('html'), 'html\n')
    self.assertEqual(tpl.render('text'), 'text\n')
    self.assertEqual(tpl.render('csv'), 'text\n')
    self.assertEqual(tpl.meta.formats, ['html', 'text', 'csv'])

  #----------------------------------------------------------------------------
  def test_file(self):
    # TODO: this test will only work if TemplateAlchemy is not zipped...
    #       not quite sure how to test the 'file' source in zipped package.
    root = templatealchemy.Template(
      source='file:' + os.path.join(os.path.dirname(__file__), 'test_data', 'mako'),
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
  def test_sqlalchemy(self):
    # todo: what if templatealchemy is a zipped archive?...
    path = os.path.join(os.path.dirname(__file__), 'test_data/sa/source.db')
    root = templatealchemy.Template(
      source='sqlalchemy:sqlite:///' + path,
      renderer='mustache')
    tpl = root.getTemplate('document')
    out = tpl.render('html', adict(title='TemplateAlchemy'))
    chk = '<html><body><h1>TemplateAlchemy</h1></body></html>'
    out = tpl.render('text', adict(title='TemplateAlchemy'))
    chk = 'Title: TemplateAlchemy\n'
    self.assertMultiLineEqual(out, chk)
    self.assertEqual(tpl.meta.formats, ['html', 'text'])

  #----------------------------------------------------------------------------
  def test_string(self):
    root = templatealchemy.Template(source='string:ALL YOUR ${plan["from"]} ARE BELONG TO ${plan["to"]}')
    params = dict(plan=adict((('from', 'BASE'), ('to', 'US'))))
    outt = root.render('text', params)
    outh = root.render('html', params)
    self.assertEqual(outt, 'ALL YOUR BASE ARE BELONG TO US')
    self.assertEqual(outh, 'ALL YOUR BASE ARE BELONG TO US')
    self.assertEqual(root.meta.formats, ['data'])

  #----------------------------------------------------------------------------
  def test_commandLine(self):
    from . import cli
    from StringIO import StringIO
    out = StringIO()
    tpl = '''\
<html>
 <head>
  <title>{{title}}</title>
 </head>
 <body>
  <h1>{{title}}</h1>
  <h2>{{doc.title}}</h2>
  {{#sections}}
   <h3>{{title}}</h3>
   <p>{{text}}</p>
  {{/sections}}
 </body>
</html>
'''
    cli.main([
        '--params',
        '{title: "TemplateAlchemy", doc: {title: "Command Line"}, sections: ['
        + '{title: Overview, text: Good},'
        + '{title: Details, text: Poor},'
        + '{title: Utility, text: Excellent},'
        + ']}',
        '--renderer', 'mustache',
        'string:' + tpl], output=out)
    chk = '''\
<html>
 <head>
  <title>TemplateAlchemy</title>
 </head>
 <body>
  <h1>TemplateAlchemy</h1>
  <h2>Command Line</h2>
   <h3>Overview</h3>
   <p>Good</p>
   <h3>Details</h3>
   <p>Poor</p>
   <h3>Utility</h3>
   <p>Excellent</p>
 </body>
</html>
'''
    self.assertMultiLineEqual(out.getvalue(), chk)

  #----------------------------------------------------------------------------
  def test_meta(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mustache',
      renderer='mustache')
    tpl = root.getTemplate('meta-simple')
    self.assertEqual(tpl.meta.formats, [])
    self.assertTrue('attachments' in tpl.meta)
    self.assertEqual(len(tpl.meta.attachments), 2)
    self.assertEqual(tpl.meta.attachments, [
      dict(name='logo.txt', cid=True, content='My Logo'),
      dict(name='logo.png', cid=True, content='\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\n\x00\x00\x00\n\x01\x03\x00\x00\x00\xb7\xfc]\xfe\x00\x00\x00\x06PLTE\xff\xff\xff\x00\x00\x00U\xc2\xd3~\x00\x00\x00\tpHYs\x00\x00\x0fa\x00\x00\x0fa\x01\xa8?\xa7i\x00\x00\x00\x07tIME\x07\xdd\x07\x07\x12\x04\x11\\\xfd\xd3\x10\x00\x00\x00 IDAT\x08\xd7c\xb0g`\xa8o`x{\x80\xe1\x0c\x18\xdd;\xc0\xf0\xff\x00\x88\x0b\x14\xb4g\x00\x00\xb8(\x0cL\xa6v\x1f\xd8\x00\x00\x00\x00IEND\xaeB`\x82'),
      ])

  #----------------------------------------------------------------------------
  def test_mako_context(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mako',
      renderer='mako',
      extmap={'text': 'txt'})
    tpl = root.getTemplate('sub')
    out = tpl.render('html', dict(text='some text'))
    chk = '''\
<!DOCTYPE html>
<html>
 <head>
  <title>SubTemplate</title>
 </head>
 <body>
  <h1>Base Common Section</h1>
  

<p>
 Some sub-template content: some text.
</p>

 </body>
</html>
'''
    self.assertMultiLineEqual(out, chk)

  #----------------------------------------------------------------------------
  def test_source_override(self):
    root = templatealchemy.Template(
      source='pkg:templatealchemy:test_data/mustache',
      renderer='mustache')
    src = templatealchemy.loadSource('string:Short: {{title}}')
    tpl = root.getTemplate(src)
    out = tpl.render('html', adict(
        title='TemplateAlchemy',
        doc=adict(title='Mustache'),
        sections=[
          adict(title='Overview', text='Good'),
          adict(title='Details', text='Poor'),
          adict(title='Utility', text='Excellent'),
          ]))
    chk = 'Short: TemplateAlchemy'
    self.assertMultiLineEqual(out, chk)
    self.assertEqual(tpl.meta.formats, ['data'])


#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
