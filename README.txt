# genedata

IMPORTANT: genedata is in its very early stages - you should come back
later.

The ``genedata`` package provides a generic abstraction to providing
template-based rendered data. The primary purpose of this package is
to allow other packages that need templated data (such as the email
generation package `genemail`) to remain un-opinionated about template
format and source, while still providing useful higher-level
functionality.

By default, genedata uses pkgutil for template location (i.e. files
from a package, either on the filesystem or in a zip archive) and Mako
for rendering, but these settings are trivial to configure to use
something else. For example, you may want to store templates in a
database (built-in support) and use the Jinja2 rendering engine
(supported via the genedata-jinja2 package).


## TL;DR

Install:

``` bash
$ pip install genedata
```

Use:

``` python

import genedata

# create a top-level template
root = genedata.Template(
  source = 'pkg:mypackagename:lib/templates',
  renderer = 'mako',
  )

# load the template in 'mypackagename:lib/templates/foo'
foo = root.getTemplate('foo')

# render the 'text' version with some parameters
params = dict(value='bar', zig='zog')
text = foo.render('text', params)

# get meta information about the template
if 'attachments' in foo.meta.maps:
   for attachment in foo.getMap('attachments'):
     # ... do something with each attachment

# supported formats are stored in meta.formats
assert(foo.meta.formats == ['text', 'html'])

```


## Overview

The primary API exposed by genedata is the *genedata.Template*. A
template has two functions:

* Generate content: given a requested format and parameters, a
  template renders serialized output data.

* Expose meta-information: certain constructs, such as email
  generation and generated data previews, require that the template
  disclose some kinds of information. Basically, template management
  is a *duplex* data stream.

In order to achieve these functions, templates use *sources* and
*renderers*. Sources provide read access to persistent storage and
renderers convert source data into output form.


### Sources

Although genedata comes with several built-in template sources, it
exposes a generic API that can be extended to support any template
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


### Renderers

Once a template has been loaded from a source, it is rendered to
serialized form by a renderer. Just like sources, genedata uses an
abstract interface for this function, and therefore can support any
rendering engine, but genedata has support for the following engines
out of the box:

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

## API Details

This section provides in-depth API information.

### Sources

#### Abstract Interface

The abstract interface for a genedata source is in
`genedata.api.Source`, which has the following signature:

``` python
class genedata.api.Source(object):

  def get(self, format):
    '''
    Returns the source content for the current template
    source for the specified `format`.
    '''

  def getSource(self, name):
    '''
    Returns a subsidiary source template, relative to the current
    template, with the specified `name`. This is seen as a hierchical
    relationship, and is typically represented as a slash ('/')
    delimited path.
    '''
```

#### File Hierarchy ('file' and 'pkg' sources)

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
archived in a zip egg archive, but will be treated the same.) When
rendering, the `format` maps directly to the file extension, adjusted
for any `spec` rules.

For example, given the following filesystem structure:

```
-- /myroot/
   `-- foo/
       |-- bar.html      | content: '<html><p>{{name}}</p></html>'
       `-- bar.text      | content: 'Name is {{name}}'
```

The following code will pass the assert:

``` python
import genedata
root = genedata.Template(source='file:/myroot', renderer='mustache')
foo  = root.getTemplate('foo')
bar  = foo.getTemplate('bar')  # or root.getTemplate('foo/bar')

assert(bar.render('text', dict(name='Joe')) == 'Name is Joe')
assert(bar.render('html', dict(name='Joe')) == '<html><p>Joe</p></html>')
```

#### SQLAlchemy

The `sqlalchemy` source allows templates to be store in any database
that the SQLAlchemy python library supports. The sqlalchemy
specification is simply the database URL as you would pass it to
sqlalchemy.create_engine.  For example, if the templates were stored
in the /var/lib/templates.db sqlite database, then the `source` spec
should be ``sqlalchemy:sqlite:////var/lib/templates.db``.

By default, the sqlalchemy source expects a table named ``template``
to exist in the database, with the column names `name`, `format` and
`content`. Currently, the `genedata.sqlalchemy` implementation does not
support the use of sessions; to use them instead of the standard
direct connection, use a subclass of `genedata.sqlalchemy.SaSource`.

For example, given the following database content:

```
$ sqlite3 -header -column /var/lib/templates.db 'select * from template'
name        format      content                                     
----------  ----------  ----------------------------
foo/bar     html        <html><p>{{name}}</p></html>
foo/bar     text        Name is {{name}}
```

The following code will pass the assert:

``` python
import genedata
root = genedata.Template(source='sqlalchemy:sqlite:////var/lib/templates.db',
                         renderer='mustache')
foo  = root.getTemplate('foo')
bar  = foo.getTemplate('bar')  # or root.getTemplate('foo/bar')

assert(bar.render('text', dict(name='Joe')) == 'Name is Joe')
assert(bar.render('html', dict(name='Joe')) == '<html><p>Joe</p></html>')
```


### Renderers

#### Abstract Interface

The abstract interface for a genedata renderer is in
`genedata.api.Renderer`, which has the following signature:

``` python
class genedata.api.Renderer(object):

  def render(self, context, data, params):
    '''
    Renders the given template `data` (as a binary blob of data)
    with the given `params`, which should be typically passed to
    the template as variables using a template-specific mechanism.

    todo: update this when the time comes:

    `context` is a reserved parameter that is intended to enable
    cross-driver optimizations, but has not been defined at this
    point.
    '''
```


#### Mako

TODO: add docs


#### Mustache

TODO: add docs
