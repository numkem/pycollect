import requests
from lib.command import Command


class VgcollectCommand(Command):
    excluded_category_id = ['29', '380', '381', '382', '383',
                            '384', '385', '386', '387']
    api_base_url = "http://api.vgcollect.com"
    api_key = 'abcdefg'

    def __init__(self, *args, **kwargs):
        self.register_command('search', VgcollectSearchCommand, shortcuts=['s'])
        self.register_command('info', VgcollectInfoCommand, shortcuts=['i'])


class VgcollectInfoCommand(VgcollectCommand):
	def run(self):
		r = requests.get('/'.join([self.api_base_url, 'items', 
						 self.args[0], self.api_key]))
		if r.status_code == 200 and len(r.json()):
			data = r.json()

			for key, value in data['results'].iteritems():
				print('{}: {}'.format(self.underscore_camel_case_space(key), value))
		else:
			print("No result found.")


class VgcollectSearchCommand(VgcollectCommand):
    result_header = ['ID', 'Category', 'Name']

    def run(self):
        r = requests.get(
            '/'.join([self.api_base_url, 'search', '+'.join(self.args),
                     self.api_key]))
        if r.status_code == 200 and len(r.json()):
            data = r.json()

            results = []
            for item in data:
                if item['category_id'] not in self.excluded_category_id:
                    results.append([item['game_id'], item['category_name'],
                                   item['name']])
            self.show_results(results)
        else:
            print("No result found.")


class VgcollectAddDatabaseCommand(VgcollectCommand):
    db = None

    def run(self, dbFilename):
        


main_class = VgcollectCommand
