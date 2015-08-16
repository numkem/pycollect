import requests
from lib.command import Command
from lib.models import Game


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
    def help(self):
        self.showHelp('add', '<ID from search command>',
                      'This command adds the item specified into the internal database.')

    def run(self):
        try:
            if not self.args[0].isdigit:
                self.show_help()
            item = self.get_item(self.args[0])
            game = Game(item)
            self.db.save(game)
            self.db.commit()
            self.success("Game added")
        except IndexError:
            self.help()
        except KeyError:
            self.error("No result found")



class VgcollectInfoCommand(VgcollectCommand):
    def run(self):
        try:
            item = self.get_item(self.args[0])

            for key, value in item.iteritems():
                print('{}: {}'.format(self.underscore_camel_case_space(key), value))
        except KeyError:
            self.error("No result found")


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
