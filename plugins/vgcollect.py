import requests
from blessings import Terminal

from lib.command import Command, UsageException

term = Terminal()


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

    def run(self):
        try:
            if not self.args[0].isdigit:
                raise UsageException()
        except IndexError:
            raise UsageException()
        item = self.get_item(self.args[0])

        # Check if the game is already in the database
        if self.db.games.find_one({'id:': self.args[0]}) is None:
            self.db.games.insert_one(item)

            self.success("Game added")
        else:
            self.error("Game already in database, try editing it instead.")


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
                                results.append([item['game_id'], item['category_name'],
                                                item['name']])
                        else:
                            results.append([item['game_id'], item['category_name'],
                                            item['name']])
                except KeyError:
                    pass
            self.show_results(results)
        except TypeError:
            self.error("No results found")


main_class = VgcollectCommand
