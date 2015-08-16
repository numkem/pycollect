from prettytable import PrettyTable


class Command(object):
    result_header = ['ID', 'Category', 'Name']
    args = []
    commands = {}
    shortcuts = {}
    db = None

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

    def underscore_camel_case_space(self, string):
        return ' '.join([w.capitalize() for w in string.split('_')])

    def get_commands(self):
        return self.commands

    def show_help(self, command, args, help_msg):
        print("{} {}\n\n{}".format(command, args, help_msg))
