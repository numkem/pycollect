import requests
from blessings import Terminal
from tinydb import where

from lib.command import Command, UsageException
from pycollect import db

term = Terminal()
games = db.table('games')

class VgcollectCommand(Command):
    excluded_category_id = ['29', '380', '381', '382', '383',
                            '384', '385', '386', '387']
    api_base_url = "http://api.vgcollect.com"
    api_key = 'abcdefg'

    def __init__(self, *args, **kwargs):
        self.register_command('search', VgcollectSearchCommand, shortcuts=['se'])
        self.register_command('info', VgcollectInfoCommand, shortcuts=['in'])
        self.register_command('add', VgcollectAddCommand, shortcuts=['ad'])


    def search_items(self, args):
        r = requests.get(
            '/'.join([self.api_base_url, 'search', '+'.join(args),
                     self.api_key]))
        if r.status_code == 200 and len(r.json()):
            return r.json()
        else:
            return None

    def get_item(self, item_id):
        r = requests.get('/'.join([self.api_base_url, 'items',
                                   item_id, self.api_key]))
        if r.status_code == 200 and len(r.json()):
            return r.json()['results']


class VgcollectAddCommand(VgcollectCommand):
    help_command = 'add'
    help_args = ['ID from search command']
    help_msg = \
        """
        This command adds the item specified into the internal database.
        """

    """
    extract_fields: Check all the fields given to the command for a pattern
        like key=value
    """
    def extract_fields(self, arguments):
        fields = {}
        items = []
        for arg in self.args:
            try:
                if '=' in arg:
                    key, value = arg.split('=')
                    fields[key] = value
                if arg.isdigit():
                    items.append(arg)
            except ValueError:
                raise UsageException
        return (items, fields)

    def run(self):
        # Fields can be set in the format key=value, they will be added to
        # the game
        item_ids, fields = self.extract_fields(self.args)

        if not len(item_ids):
            raise UsageException()

        for item_id in item_ids:
            item = self.get_item(item_id)

            # Check if the game is already in the database
            if len(games.search(where('id') == item_id)):
                self.error("Game #{} already in database.".format(item_id))
            else:
                games.insert(item)
                if bool(fields):
                    games.update(fields, where('id') == item_id)

                self.success("Game #{} added.".format(item_id))


class VgcollectInfoCommand(VgcollectCommand):
    help_command = 'info'
    help_args = ['ID from search command']
    help_msg = \
        """
        Show all details of an item from the remote database.
        """

    def run(self):
        item = self.get_item(self.args[0])
        self.show_dict(item)


class VgcollectSearchCommand(VgcollectCommand):
    help_command = 'search'
    help_args = ['keywords to search for']
    help_msg = \
        """
        Search remote database for games with the provided keywords.

        Filtering by console name can be done by using the a '|'.
        Examples:
            search halo | xbox
            search halo | xbox360
        """
    result_header = ['ID', 'Category', 'Name']

    def run(self):
        # If there is a pipe in the search params,
        # we filter using the console name.
        if '|' in self.args:
            args = self.args[:self.args.index('|')]
            filters = self.args[self.args.index('|')+1:]
        else:
            args = self.args
            filters = []

        try:
            data = self.search_items(args)
            results = []
            for item in data:
                try:
                    if item['category_id'] not in self.excluded_category_id:
                        if len(filters):
                            if item['category_slug'] in filters:
                                results.append([item['game_id'],
                                                item['category_name'],
                                                item['name']])
                        else:
                            results.append([item['game_id'],
                                            item['category_name'],
                                            item['name']])
                except KeyError:
                    pass
            self.show_results(results)
        except TypeError:
            self.error("No result found.")


main_class = VgcollectCommand
