#!/usr/bin/env python
from __future__ import print_function
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from prompt_toolkit.contrib.completers import WordCompleter
from pluginbase import PluginBase
from tinydb import TinyDB
import click
import sys
import os

from lib.command import UsageException
from lib.command import Command


DEFAULT_DB_FILENAME = os.path.join(os.getcwd(), 'pycollect.db')
PLUGIN_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'plugins')

db = TinyDB(DEFAULT_DB_FILENAME)

def run(command, text):
    command.parse(text)
    command.run()

@click.command()
def main():
    plugin_base = PluginBase(package="pycollect.plugins")
    plugin_source = plugin_base.make_plugin_source(
        searchpath=[PLUGIN_DIR])
    history = History()
    all_commands = dict()
    all_shortcuts = dict()

    # Load all plugins
    with plugin_source:
        for file in os.listdir(PLUGIN_DIR):
            if '.py' in file and '.pyc' not in file:
                mod = plugin_source.load_plugin(file.replace('.py', ''))
                cmd = mod.main_class()

                # Add the registered commands to the commands dict
                all_commands.update(cmd.commands)
                all_shortcuts.update(cmd.shortcuts)
    while True:
        text = get_input(u'> ', history=history,
                         completer=WordCompleter(all_commands.keys()))

        cmd_name = text.split(' ')[0]
        command = None
        if cmd_name in all_commands:
            command = all_commands[cmd_name]
        elif cmd_name in all_shortcuts:
            command = all_shortcuts[cmd_name]
        else:
            Command.error("Command not found.")

        try:
            if command is not None:
                run(command(), text)
        except UsageException:
            command.help()
        except KeyboardInterrupt:
            pass
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()
