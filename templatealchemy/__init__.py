# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/29
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

try:
  __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
  __path__ = __import__('pkgutil').extend_path(__path__, __name__)

# todo: ugh. this is ugly, but there is just no other way to make
#       templatealchemy.driver a namespace package *AND* provide
#       useful functionality in the `templatealchemy` module...
#       basically, every TA driver provider *MUST* have a copy of this
#       file as the templatealchemy/__init__.py file.
#
#       yuck.

try:
  from templatealchemy.common import *
except ImportError:
  pass

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
