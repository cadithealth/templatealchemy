===============
TemplateAlchemy
===============

.. WARNING::

  2013/07/29: TemplateAlchemy is in its very early stages - you should
  come back later.

TemplateAlchemy aims to be to the fragmented world of templates what
SQLAlchemy is to the world of databases: a generic abstraction for
systems that need templated data, but don't care about what language
or implementation is used to render that data.

In essence, the primary purpose of this package is to allow other
packages that need templated data (such as the email generation
package `genemail <https://pypi.python.org/pypi/genemail>`_) to remain
un-opinionated about template format and source, while still providing
useful higher-level functionality.

By default, TemplateAlchemy uses pkgutil for template location
(i.e. files from a package, either on the filesystem or in a zip
archive) and Mako for rendering, but these settings are trivial to
configure to use something else. For example, you may want to store
templates in a database (with built-in support) and use the Jinja2
rendering engine (supported via the `TemplateAlchemy-Jinja2
<https://pypi.python.org/pypi/TemplateAlchemy-Jinja2>`_ package).


TL;DR
=====

Install:

.. code-block:: bash

  $ pip install templatealchemy

Use:

.. code-block:: python

  import templatealchemy as ta

  # create a top-level template manager
  root = ta.Manager(
    source = 'pkg:mypackagename:lib/templates',
    renderer = 'mako',
    )

  # load the sub-template 'foo'
  foo = root.getTemplate('foo')

  # render the 'text' version with some parameters; the
  # actual template is then in 'mypackagename:lib/templates/foo.text'
  params = dict(value='bar', zig='zog')
  text = foo.render('text', params)

  # get meta information about the template
  if 'attachments' in foo.meta:
     for attachment in foo.meta.attachments:
       # ... do something with each attachment

  # supported formats are stored in meta.formats
  assert(foo.meta.formats == ['text', 'html'])


Overview
========

The primary API exposed by TemplateAlchemy is the
*templatealchemy.Template*. A template has two functions:

* **Generate content**: given a requested format and parameters, a
  template renders serialized output data.

* **Expose meta-information**: certain constructs, such as email
  generation and generated data previews, require that the template
  disclose some kinds of information. Basically, templates can provide
  additional information to give context to the template.

In order to achieve these functions, templates use *sources* and
*renderers*. Sources provide read access to persistent storage and
renderers convert source data into output form.

.. IMPORTANT::

  The special format ``spec`` is reserved and used to parameterize
  template meta information; it must not be used as a format.


Sources
-------

Although TemplateAlchemy comes with several built-in template sources,
it exposes a generic API that can be extended to support any template
storage mechanism. The following built-in sources exist:

* ``file``:

  Fetches templates from the filesystem. See `API Details`_ for more
  information.

* ``pkg``:

  The `pkg` source extracts sources from a python package. This means
  that it can stream the data directly from the filesystem or from a
  zip-archive (depending on how the package was installed). See `API
  Details`_ for more information.

* ``sqlalchemy``:

  The `sqlalchemy` source fetches sources from a database using the
  SQLAlchemy database abstraction library. See `API Details`_ for more
  information.

* ``stream``:

  The `stream` source reads a template from a file-like object;
  because it does not buffer any data, the template is single-use.
  This is typically used in programs that know that the template will
  only be used once, such as command-line programs.

* ``string``:

  The `string` source allows a simple way to provide templates inline.
  Generally not very useful beyond that -- serious re-evaluation is
  recommended if this is used frequently in an application.


Renderers
---------

Once a template has been loaded from a source, it is rendered to
serialized form by a renderer. Just like sources, TemplateAlchemy uses
an abstract interface for this function, and therefore can support any
rendering engine. TemplateAlchemy has support for the following
engines built-in:

* ``mako``:

  Probably the most efficient and most advanced python templating
  engine, mako is the recommended engine. However, it does allow
  arbitrary python to be executed, so the input data must be trusted.
  See `API Details`_ for more information.

* ``mustache``:

  A logic-less templating engine that is very simple and effective.
  Since it does not allow arbitrary python to be executed, this is a
  better choice of renderer if the input data is not trusted. See `API
  Details`_ for more information.


API Details
===========

This section provides in-depth API information. Both sources and
renderers can be passed to TemplateAlchemy either as an implementation
of the respective API objects or as string specifications. In the
latter case, the string must be in the format ``TYPE:SPEC``, for
example ``"mako:default_filters=[h]"``. The ``:SPEC`` can be left off
to use default values, for example ``"mako"``.

Sources
-------

Abstract Interface
~~~~~~~~~~~~~~~~~~

The abstract interface for a TemplateAlchemy source is in
`templatealchemy.api.Source`, which has the following definition:

.. code-block:: python

  class templatealchemy.api.Source(object):

    def get(self, format):
      '''
      Returns the source content stream for the current template
      source for the specified `format`. The returned object must be a
      file-like object supporting read access.
      '''

    def getSource(self, name):
      '''
      Returns a subsidiary source template, relative to the current
      template, with the specified `name`. This is seen as a hierchical
      relationship, and is typically represented as a slash ('/')
      delimited path.
      '''

    def getFormats(self):
      '''
      Returns a list of all the available formats for this source.
      '''

    def getRelated(self, name):
      '''
      Returns a content stream for the related object `name` that
      is relative to the current template. Typically this is used
      for meta-information *spec* definitions using the "!include"
      or "!include-raw" directives. As with :meth:`get`, the
      returned object must be a file-like object supporting read
      access.
      '''


File Hierarchy ('file' and 'pkg' sources)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `file` source expects the path to the template hierarchy as a
specification, e.g. if the templates are located in
``/var/lib/templates``, then the `source` spec should be
``file:/var/lib/templates``.

The `pkg` source expects the package name and relative path to the
template hierarchy as a specification separated by a colon (':'),
e.g. if the templates are located in the ``demo`` package and within
its ``templates`` directory, then the `source` spec should be
``pkg:demo:templates``.

Template hierarchies for the `file` and `pkg` sources map directly to
filesystem hierarchies. (Note that for the `pkg` source, these may be
stored in a zip archive depending on installation method, but will be
treated the same.) When rendering, the `format` maps directly to the
file extension, adjusted for any `spec` rules.

For example, given the following filesystem structure:

.. code-block:: text

  -- /myroot/
     `-- foo/
         |-- bar.html      | content: '<html><p>{{name}}</p></html>'
         `-- bar.text      | content: 'Name is {{name}}'


The following code will pass the assert:

.. code-block:: python

  import templatealchemy as ta
  root = ta.Manager(source='file:/myroot', renderer='mustache')
  bar  = root.getTemplate('foo/bar')

  assert(bar.render('text', dict(name='Joe')) == 'Name is Joe')
  assert(bar.render('html', dict(name='Joe')) == '<html><p>Joe</p></html>')


SQLAlchemy
~~~~~~~~~~

The `sqlalchemy` source allows templates to be store in any database
that the SQLAlchemy python library supports. The sqlalchemy
specification is simply the database URL as you would pass it to
sqlalchemy.create_engine.  For example, if the templates were stored
in the /var/lib/templates.db sqlite database, then the `source` spec
would be ``sqlalchemy:sqlite:////var/lib/templates.db``.

By default, the sqlalchemy source expects a table named ``template``
to exist in the database, with the columns `name`, `format` and
`content`. Currently, the `templatealchemy.sqlalchemy` implementation
does not support the use of sessions; to use them instead of the
standard direct connection, use a subclass of
`templatealchemy.sqlalchemy.SaSource`.

For example, given the following database content:

.. code-block:: text

  $ sqlite3 -header -column /var/lib/templates.db 'select * from template'
  name        format      content
  ----------  ----------  ----------------------------
  foo/bar     html        <html><p>{{name}}</p></html>
  foo/bar     text        Name is {{name}}

The following code will pass the assert:

.. code-block:: python

  import templatealchemy as ta
  root = ta.Manager(source='sqlalchemy:sqlite:////var/lib/templates.db',
                    renderer='mustache')
  bar  = root.getTemplate('foo/bar')

  assert(bar.render('text', dict(name='Joe')) == 'Name is Joe')
  assert(bar.render('html', dict(name='Joe')) == '<html><p>Joe</p></html>')


Renderers
---------

Abstract Interface
~~~~~~~~~~~~~~~~~~

The abstract interface for a TemplateAlchemy renderer is in
`templatealchemy.api.Renderer`, which has the following definition:

.. code-block:: python

  class templatealchemy.api.Renderer(object):

    def render(self, context, stream, params):
      '''
      Renders the given template data `stream` (as a read-access
      file-like object) to serialized rendered output. The given
      `params` provide variables that are typically passed to the
      template using template-specific mechanisms.

      todo: update this when the time comes:

      `context` is a reserved parameter that is intended to enable
      cross-driver optimizations, but has not been defined at this
      point.
      '''


Mako
~~~~

TODO: add docs


Mustache
~~~~~~~~

TODO: add docs
