#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/03
# copy: (C) Copyright 2013 Cadit Inc., see LICENSE.txt
#------------------------------------------------------------------------------

import os, sys, re
from setuptools import setup, find_packages

# require python 2.7+
assert(sys.version_info[0] > 2
       or sys.version_info[0] == 2
       and sys.version_info[1] >= 7)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

test_requires = [
  'nose                 >= 1.2.1',
  'coverage             >= 3.5.3',
  ]

requires = [
  'distribute           >= 0.6.24',
  'PyYAML               >= 3.10',
  # TODO: make these only dependencies if they are actually wanted...
  'SQLAlchemy           >= 0.8.1',
  'Mako                 >= 0.7.2',
  'MarkupSafe           >= 0.15',
  'pystache             >= 0.5.3',
  # 'Markdown             >= 2.3.1',
  ]

entrypoints = {
  'console_scripts': [
    'ta-eval            = templatealchemy.cli:main',
    ],
  }

setup(
  name                  = 'TemplateAlchemy',
  version               = '0.1.18',
  description           = 'An un-opinionated template abstraction layer',
  long_description      = README,
  classifiers           = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'License :: Public Domain',
    ],
  author                = 'Philip J Grabner, Cadit Health Inc',
  author_email          = 'oss@cadit.com',
  url                   = 'http://github.com/cadithealth/templatealchemy',
  keywords              = 'template unopinionated abstraction layer sqlalchemy mako mustache',
  packages              = find_packages(),
  namespace_packages    = ['templatealchemy_driver'],
  include_package_data  = True,
  zip_safe              = True,
  install_requires      = requires,
  tests_require         = test_requires,
  test_suite            = 'templatealchemy',
  entry_points          = entrypoints,
  license               = 'MIT (http://opensource.org/licenses/MIT)',
  )

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
