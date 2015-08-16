from lib.command import Command
from lib.models import *


class DatabaseCommand(Command):
    def __init__(self):
        self.register_command('list', DatabaseListCommand)
        self.register_command('delete', DatabaseDeleteCommand)
        self.register_command('show', DatabaseShowCommand)


class DatabaseListCommand(Command):
    def run(self):
        try:
            all_games = self.db.filter(Game, {})
            results = [(g.id, g.platform, g.name) for g in all_games]
            self.show_results(results)
        except Game.DoesNotExist:
            print("Database doesn't contain any games.")


class DatabaseDeleteCommand(Command):
    def help(self):
        self.show_help("delete", "<ID of game>",
                       "Delete the game matching the ID given from the database.")

    def run(self):
        try:
            game = self.db.get(Game, {'id': self.args[0]})
            self.db.delete(game)
            self.db.commit()
            print("Game deleted")
        except Game.DoesNotExist:
            print("No game matching this ID exists in the database")
        except KeyError:
            self.help()


class DatabaseShowCommand(Command):
    def help(self):
        self.show_help("show", "<ID of game>",
    		           "Show all the data from a game already in the database.")

    def run(self):
        try:
            game = dict(self.db.get(Game, {'id': self.args[0]}))
            for key, value in game.iteritems():
                print('{}: {}'.format(self.underscore_camel_case_space(key), value))
        except Game.DoesNotExist:
            print("No game matching this ID exists in the database")
        except KeyError:
            self.help()


main_class = DatabaseCommand
