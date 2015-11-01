from prettytable import PrettyTable
from blessings import Terminal
import re

term = Terminal()


class Command(object):
    result_header = ['ID', 'Category', 'Name']
    args = []
    commands = {}
    shortcuts = {}

    def parse(self, text="", **kwargs):
        self.args = text.split(' ')[1:]

        [setattr(self, key, value) for key, value in kwargs.iteritems()]

    def show_results(self, results):
        table = PrettyTable(self.result_header)
        table.align['Name'] = 'l'
        table.align['Category'] = 'l'
        for item in results:
            table.add_row(item)

        print(table)
        print("{} results found.".format(len(results)))

    def run(self):
        print("Not implemented!")

    def register_command(self, command, cmdObj, shortcuts=[]):
        self.commands[command] = cmdObj

        for s in shortcuts:
            self.shortcuts[s] = cmdObj

    def _regex_search_ignorecase(self, input, needle):
        return re.search(needle, input, re.IGNORECASE)

    def underscore_camel_case_space(self, string):
        return ' '.join([w.capitalize() for w in string.split('_')])

    def get_commands(self):
        return self.commands

    def show_help(self, command, args, help_msg):
        args_str = " ".join(["<{}>".format(a) for a in args])
        print("{} {}\n{}".format(command, args_str, help_msg))

    def help(self):
        self.show_help(self.help_command, self.help_args, self.help_msg)

    @classmethod
    def success(self, msg):
        print(term.green(msg))

    @classmethod
    def error(self, msg):
        print(term.red(msg))

    def show_dict(self, d):
        for key, value in d.iteritems():
            print('{}{}:{} {}'.format(term.blue,
                                      self.underscore_camel_case_space(key),
                                      term.normal, value))


class UsageException(Exception):
    pass
