#!/usr/bin/env python2
from __future__ import print_function
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from prompt_toolkit.contrib.completers import WordCompleter
from pluginbase import PluginBase
import click
import sys

sys.path.insert(0, './lib')


@click.command()
@click.argument('module')
def main(module):
    plugin_base = PluginBase(package="pycollect.plugins")
    plugin_source = plugin_base.make_plugin_source(
        searchpath=['./plugins'])
    history = History()

    while True:
        try:
            with plugin_source:
                mod = plugin_source.load_plugin(module)
                cmd = mod.main_class()

                # Register default commands so we can exit
                cmd.register_command('exit', sys.exit)
                cmd.register_command('quit', sys.exit)

                text = get_input(u'> ', history=history,
                                 completer=WordCompleter(cmd.commands.keys()))
                command = cmd.commands.get(text.split(' ')[0])()

                command.parse(text)
                command.run()
        except TypeError:
            print("Error: Command not found!")
        except KeyboardInterrupt:
            pass
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()
