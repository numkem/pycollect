from prettytable import PrettyTable


class Command(object):
    result_header = ['ID', 'Category', 'Name']
    args = []
    commands = {}

    def parse(self, text=""):
        self.args = text.split(' ')[1:]

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

    def register_command(self, command, cmdObj):
        self.commands[command] = cmdObj
        
    def underscore_camel_case_space(self, string):
    	return ' '.join([w.capitalize() for w in string.split('_')])

	def get_commands(self):
		return self.commands