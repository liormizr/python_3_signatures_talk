#!/usr/bin/env python
"""
Error Handling Hints & Tricks

Usage:
  talk.py --version
  talk.py (-h | --help)
  talk.py start
  talk.py calling_conventions

Options:
  --version     Show talk version.
  -h --help     Show talk menu and examples.
"""
import sys
import logging
import inspect

from docopt import docopt

from IPython import embed
from IPython.core.autocall import ExitAutocall
from IPython.terminal.ipapp import load_default_config

from signatures_talk import talk_map

_ipython_config = load_default_config()
_ipython_config.InteractiveShellEmbed = _ipython_config.TerminalInteractiveShell
_ipython_config.TerminalInteractiveShell.banner1 = ''
_ipython_config.TerminalInteractiveShell.banner2 = '\x1b[2J\x1b[H'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def _run_all():
    for example_suite_name, suite in talk_map.items():
        _run_suite(example_suite_name, suite)


def _run_suite(suite_name, suite):
    for index, example in enumerate(suite['examples']):
        N = Next = ExitAutocall()
        globals()[example.__name__] = example
        embed(
            header=_create_header(suite_name, suite, index, example),
            config=_ipython_config)


def _create_header(suite_name, suite, index, example):
    return (
        f'| {suite_name.title()}:\n'
        f'| Sources: {suite["sources"]}\n'
        f'|\n'
        f'| {suite_name} - {index + 1}.\n'
        f'{_code_example(example)}\n'
        f'| What will happen? >> {example.__name__}()\n'
        f'| Press "N" or "Next" to go to the next example\n'
    )


def _code_example(example):
    return '\n'.join(
        f'|    >> {line}'
        for line in inspect.getsource(example).splitlines()
    )


if __name__ == '__main__':
    talk_options = docopt(__doc__, version='0.0.1')
    try:
        if talk_options['start']:
            _run_all()
            sys.exit(0)
        for suite_name, show in talk_options.items():
            if show:
                _run_suite(suite_name, talk_map[suite_name])
    except (KeyboardInterrupt, SystemExit):
        print()
    print('Goodbye')
