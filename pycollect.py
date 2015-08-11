#!/usr/bin/env python2
from __future__ import print_function
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from prompt_toolkit.contrib.completers import WordCompleter
from pluginbase import PluginBase
import click
import sys
import os


@click.command()
def main():
    plugin_base = PluginBase(package="pycollect.plugins")
    plugin_source = plugin_base.make_plugin_source(
        searchpath=['./plugins'])
    history = History()
    all_commands = dict()

	# Load all plugins
    with plugin_source:
        for file in os.listdir('./plugins'):
            if '.py' in file and '.pyc' not in file:
				mod = plugin_source.load_plugin(file.replace('.py', ''))
				cmd = mod.main_class()
				
				# Add the registered commands to the commands dict
				all_commands.update(cmd.commands)
    while True:
        try:
            text = get_input(u'> ', history=history,
                             completer=WordCompleter(all_commands.keys()))
            command = cmd.commands.get(text.split(' ')[0])()

            command.parse(text)
            command.run()
        #except TypeError:
        #    print("Error: Command not found!")
        except KeyboardInterrupt:
            pass
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()
