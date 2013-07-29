# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  templatealchemy.cli
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/06
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import sys, argparse, yaml, os.path
from . import engine
from templatealchemy_driver import stream

#------------------------------------------------------------------------------
def main(args=None, output=None):

  cli = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
Command-line template evaluator using the TemplateAlchemy template abstraction
layer.
''',
    epilog='''\
Examples:

  # using shell pipelines with mustache rendering
  $ echo 'Hello, {{name}}!' | %(prog)s -y "{name: World}" -r mustache
  Hello, World!

  # using a file source with mustache rendering
  $ echo 'Hello, {{name}}!' > sample.text
  $ %(prog)s -y "{name: World}" -r mustache ./sample.text
  Hello, World!

  # using a sqlite3 source and mako rendering (the default)
  $ sqlite3 templates.db 'CREATE TABLE template (name VARCHAR, format VARCHAR, content TEXT);'
  $ sqlite3 templates.db 'INSERT INTO template VALUES ("foo/bar", "text", "Hello, ${name}!");'
  $ %(prog)s -y "{name: World}" -n foo/bar -f text sqlalchemy:sqlite:///templates.db
  Hello, World!
''')

  cli.add_argument(
    '-v', '--verbose',
    action='count',
    help='enable verbose output (multiple invocations increase verbosity)')

  cli.add_argument(
    '-n', '--name', metavar='NAME',
    default=None, action='store',
    help='set the template name; if omitted, the root template will be used')

  cli.add_argument(
    '-f', '--format', metavar='FORMAT',
    default=None, action='store',
    help='set the output format; if omitted, it will use the template\'s'
    ' default format')

  cli.add_argument(
    '-p', '--param', metavar='NAME=VALUE',
    default=[], action='append',
    help='set a template variable where `VALUE` is taken as a literal'
    ' string (overrides any values set in `--params`)')

  cli.add_argument(
    '-y', '--params', metavar='YAML',
    default=[], action='append',
    help='specifies a YAML-encoded dictionary as template variables;'
    ' if the value starts with the letter "@", the rest is the file name to'
    ' read as a YAML structure. If the value is exactly a dash ("-"), then'
    ' the YAML structure is read from STDIN. In all cases, the YAML'
    ' structure must be a dictionary')

  cli.add_argument(
    '-r', '--renderer', metavar='SPEC',
    default='mako',
    help='sets the rendering driver (default: %(default)r)')

  cli.add_argument(
    'source', metavar='SOURCE',
    nargs='?',
    help='the template source; if exactly a dash ("-") or omitted, then'
    ' the template is read from STDIN. If both params and template are read'
    ' from STDIN, then params is read first, followed by an EOF, then the'
    ' template. If the source lacks a colon (":") and it points to a normal'
    ' file, the template is read from the file. Otherwise, `source` is'
    ' interpreted as a source specification (i.e. "TYPE[:OPTIONS]")')

  options = cli.parse_args(args)

  params = dict()

  for yparam in options.params:
    if yparam == '-':
      yparam = sys.stdin.read()
    elif yparam.startswith('@'):
      with open(yparam[1:], 'rb') as fp:
        yparam = fp.read()
    try:
      yparam = yaml.load(yparam)
    except Exception:
      cli.error('could not parse YAML expression: %r'
                % (yparam,))
    if not isinstance(yparam, dict):
      cli.error('"--params" expressions must resolve to dictionaries')
    params.update(yparam)

  for kparam in options.param:
    if '=' not in kparam:
      cli.error('"--param" expressions must be in the KEY=VALUE format')
    key, value = kparam.split('=', 1)
    params[key] = value

  options.params = params
  output = output or sys.stdout

  if options.source is None or options.source == '-':
    options.source = stream.StreamSource(sys.stdin)
  elif ':' not in options.source and os.path.isfile(options.source):
    options.source = stream.StreamSource(open(options.source, 'rb'))

  template = engine.Template(
    source=options.source,
    renderer=options.renderer,
    )

  if options.name is not None:
    template = template.getTemplate(options.name)

  output.write(template.render(options.format, options.params))

  return 0

#------------------------------------------------------------------------------
if __name__ == '__main__':
  sys.exit(main())

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
