#!/usr/bin/env python
from __future__ import print_function
from prompt_toolkit.shortcuts import get_input
from prompt_toolkit.history import History
from prompt_toolkit.contrib.completers import WordCompleter
from pluginbase import PluginBase
from pymongo import MongoClient
import click
import sys
import os

from lib.command import UsageException


DEFAULT_DB_FILENAME = os.path.join(os.getcwd(), 'pycollect.db')
PLUGIN_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'plugins')


@click.option('--db', 'db_filename', default=DEFAULT_DB_FILENAME,
              help="Database filename")
@click.command()
def main(db_filename):
    plugin_base = PluginBase(package="pycollect.plugins")
    plugin_source = plugin_base.make_plugin_source(
        searchpath=[PLUGIN_DIR])
    history = History()
    all_commands = dict()
    all_shortcuts = dict()

    # Initialize database
    client = MongoClient()
    db = client['pycollect']

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
        try:
            text = get_input(u'> ', history=history,
                             completer=WordCompleter(all_commands.keys()))
            try:
                command = all_commands.get(text.split(' ')[0])()
            except TypeError:
                # Try to use a shortcut instead
                command = all_shortcuts.get(text.split(' ')[0])()

            command.parse(text, db=db)
            try:
                command.run()
            except (IndexError, KeyError):
                raise UsageException()
        except TypeError:
            print("Error: Command not found!")
        except UsageException:
            command.help()
        except KeyboardInterrupt:
            pass
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()
