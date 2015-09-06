from lib.command import Command
import re


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
        regex = re.compile(self.args[0], re.IGNORECASE)
        games = self.db.games.find({'name': regex})
        results = [(g['id'], g['platform'], g['name']) for g in games]
        self.show_results(results)


class DatabaseListCommand(Command):
    help_command = 'list'
    help_args = []
    help_msg = \
        """
        List all the games currently in the local database
        """

    def run(self):
        all_games = list(self.db.games.find())
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
        self.db.games.remove({'id': self.args[0]})
        self.success("Game deleted")


class DatabaseEditCommand(Command):
    help_command = 'edit'
    help_args = ['ID of game', 'key', 'value']
    help_msg = \
        """
        Assign the <value> to the <key> for the game provided.
        If the value doesn't exists, it will be created.
        """

    def run(self):
        game = self.db.games.find_one({'id': self.args[0]})
        if game is None:
            self.error("No game matching this ID exists in the database")
        else:
            key = self.args[1]
            value = ' '.join(self.args[2:])
            game[key] = value

            self.db.games.replace_one({'_id': game['_id']}, game)
            self.success("Game modified")


class DatabaseShowCommand(Command):
    help_command = 'show'
    help_args = ['ID of game']
    help_msg = \
        """
        Show all the data from a game already in the database.
        """

    def run(self):
        game = self.db.games.find_one({'id': self.args[0]})
        self.show_dict(game)

main_class = DatabaseCommand
