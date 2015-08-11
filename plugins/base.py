from lib.command import Command
import sys


class BaseCommand(Command):
	def __init__(self, *args, **kwargs):
		self.register_command('exit', sys.exit)
		self.register_command('quit', sys.exit)


main_class = BaseCommand