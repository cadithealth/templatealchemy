# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# lib:  genedata.cli
# auth: Philip J Grabner <grabner@cadit.com>
# date: 2013/07/06
# copy: (C) Copyright 2013 Cadit Health Inc., All Rights Reserved.
#------------------------------------------------------------------------------

import sys, argparse, yaml
from . import engine, stream

#------------------------------------------------------------------------------
def main(args=None, output=None):

  cli = argparse.ArgumentParser(
    description='''\
Command-line template compiler using the `genedata`
template abstraction layer.
''',
    epilog='''\
Example:

$ echo "My name is {{name}}." | %(prog)s -y "{name: Joe}" -r mustache
My name is Joe.
''')

  cli.add_argument(
    '-v', '--verbose',
    action='count',
    help='enable verbose output (multiple invocations increase verbosity)')

  cli.add_argument(
    '-p', '--param', metavar='NAME=VALUE',
    default=[], action='append',
    help='set a template variable where `VALUE` is taken as a literal'
    ' string (overrides any values set in `--params`)')

  cli.add_argument(
    '-f', '--format', metavar='FORMAT',
    default=None, action='store',
    help='set the output format; if omitted, it will use the template\'s'
    ' default format')

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
    ' template. Otherwise, `source` is interpreted as a genedata source'
    ' specification')


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
      cli.error('could not interpret YAML expression: %r'
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

  template = engine.Template(
    source=options.source,
    renderer=options.renderer,
    )

  output.write(template.render(options.format, options.params))

  return 0

#------------------------------------------------------------------------------
if __name__ == '__main__':
  sys.exit(main())

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
