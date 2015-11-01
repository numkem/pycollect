from lib.command import Command
from pycollect import db
from tinydb import where

games = db.table('games')

class DatabaseCommand(Command):
    def __init__(self):
        self.register_command('list', DatabaseListCommand, shortcuts=['ls'])
        self.register_command('delete', DatabaseDeleteCommand, shortcuts=['del'])
        self.register_command('show', DatabaseShowCommand, shortcuts=['sh'])
        self.register_command('edit', DatabaseEditCommand, shortcuts=['ed'])
        self.register_command('find', DatabaseFindComand, shortcuts=['fi'])


class DatabaseFindComand(Command):
    help_command = 'find'
    help_args = ['search terms']
    help_msg = \
        """
        Find a game already in the database, works like search command.
        """

    def run(self):
        local_games = games.search(where('name').matches(".*{}.*".format(self.args[0])))
        results = [(g['id'], g['platform'], g['name']) for g in local_games]
        self.show_results(results)


class DatabaseListCommand(Command):
    help_command = 'list'
    help_args = []
    help_msg = \
        """
        List all the games currently in the local database
        """

    def run(self):
        all_games = games.all()
        results = [(g['id'], g['platform'], g['name']) for g in all_games]
        self.show_results(results)


class DatabaseDeleteCommand(Command):
    help_command = 'delete'
    help_args = ['ID of game']
    help_msg = \
        """
        Delete the game matching the ID given from the database.
        """

    def run(self):
        games.remove(where('id') == self.args[0])
        self.success("Game deleted.")


class DatabaseEditCommand(Command):
    help_command = 'edit'
    help_args = ['ID of game', 'key', 'value']
    help_msg = \
        """
        Assign the <value> to the <key> for the game provided.
        If the value doesn't exists, it will be created.
        """

    def run(self):
        game = games.search(where('id') == self.args[0])[0]
        if not len(game):
            self.error("No game matching this ID exists in the database.")
        else:
            key = self.args[1]
            value = ' '.join(self.args[2:])

            games.update({key: value}, where('id') == self.args[0])
            self.success("Game modified.")


class DatabaseShowCommand(Command):
    help_command = 'show'
    help_args = ['ID of game']
    help_msg = \
        """
        Show all the data from a game already in the database.
        """

    def run(self):
        try:
            game = games.search(where('id') == self.args[0])[0]
            self.show_dict(game)
        except IndexError:
            self.error("Game #{} not in database.".format(self.args[0]))

main_class = DatabaseCommand
