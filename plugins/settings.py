from lib.command import Command
from pycollect import db
from tinydb import where

class SettingCommand(Command):
    def __init__(self):
        self.register_command('setting', SettingMainCommand, shortcuts=['set'])


class SettingMainCommand(Command):
    help_command = 'setting'
    help_args = ['command', 'options']
    help_msg = \
        """
        This command is used to modify internal option of pycollect.
        """

    def list_columns_option(self):
        try:
            columns = set_table.search(where('name') == 'settings')
        except IndexError:
            self.help()

    def run(self):
        commands = {
            'list_columns': self.list_columns_option
        }

        try:
            if self.args[0] in commands:
                commands[self.args[0]]()
        except IndexError:
            self.help()


main_class = SettingCommand
