from lib.command import Command
from lib.models import *
import re


class DatabaseCommand(Command):
    def __init__(self):
        self.register_command('list', DatabaseListCommand, shortcuts=['ls'])
        self.register_command('delete', DatabaseDeleteCommand, shortcuts=['del'])
        self.register_command('show', DatabaseShowCommand, shortcuts=['sh'])
        self.register_command('edit', DatabaseEditCommand, shortcuts=['ed'])
        self.register_command('find', DatabaseFindComand, shortcuts=['fi'])


class DatabaseFindComand(Command):
    def help(self):
        self.show_help("find", "<search terms>",
                       "Find a game already in the database, works like search command")

    def run(self):
        try:
            all_games = self.db.filter(Game, {})
            results = []
            for g in all_games:
                if re.search(".*{}.*".format(' '.join(self.args)), g.name, re.IGNORECASE):
                    results.append((g.id, g.platform, g.name))
            self.show_results(results)
        except Game.DoesNotExist:
            self.error("No results found")


class DatabaseListCommand(Command):
    def run(self):
        try:
            all_games = self.db.filter(Game, {})
            results = [(g.id, g.platform, g.name) for g in all_games]
            self.show_results(results)
        except Game.DoesNotExist:
            self.error("Database doesn't contain any games.")


class DatabaseDeleteCommand(Command):
    def help(self):
        self.show_help("delete", "<ID of game>",
                       "Delete the game matching the ID given from the database.")

    def run(self):
        try:
            game = self.db.get(Game, {'id': self.args[0]})
            self.db.delete(game)
            self.db.commit()
            self.success("Game deleted")
        except Game.DoesNotExist:
            self.error("No game matching this ID exists in the database")
        except KeyError:
            self.help()


class DatabaseEditCommand(Command):
    def help(self):
        self.show_help("edit", "<ID of game> <key> <value>",
        			   "Assign the <value> to the <key> for the game provided.\n"
                       + "If the value doesn't exists, it will be created.")

    def run(self):
        try:
            game = self.db.get(Game, {'id': self.args[0]})
            key = self.args[1]
            value = ' '.join(self.args[2:])

            setattr(game, key, value)
            self.db.save(game)
            self.db.commit()
            self.success("Game modified")
        except Game.DoesNotExist:
            self.error("No game matching this ID exists in the database")
        except (KeyError, IndexError):
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
