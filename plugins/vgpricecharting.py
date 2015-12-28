from blessings import Terminal
from tinydb import where
from tqdm import tqdm
import csv

from lib.command import Command, UsageException
from pycollect import db

term = Terminal()
games = db.table('games')
prices = db.table('vgpc_prices')

class VgPriceChartingCommand(Command):
    def __init__(self, *args, **kwargs):
        self.register_command('price_lookup', VgPriceChartingLookupCommand, shortcuts=['pl'])
        self.register_command('price_load', VgPriceChartingLoadCommand, shortcuts=['lp'])


class VgPriceChartingLoadCommand(VgPriceChartingCommand):
    help_command = "price_load"
    help_args = ['Filename of a Price Charting database']
    help_msg = \
        """
        This command loads a given Price Charting database locally.
        """
    import_keys = ('id', 'cib-price', 'loose-price', 'product-name')

    def run(self):
        try:
            with open(self.args[0]) as csvfile:
                reader = csv.DictReader(csvfile)
                all_prices = []
                for row in reader:
                    # For every game, check if the ID exists
                    p = prices.search(where('id') == row['id'])
                    if len(p):
                        # If it already exists, delete it
                        prices.remove(where('id') == row['id'])
                    all_prices.append(row)

            prices.insert_multiple(all_prices)
            self.success("Price Charting database updated")
        except IOError as e:
            self.error("Couldn't open dataabase file {}: {}".format(self.args[0], e.strerror))


class VgPriceChartingLookupCommand(VgPriceChartingCommand):
    def run(self):
        found_prices = prices.search(where('product-name').test(self._regex_search_ignorecase, r'{}'.format(self.args[0])))
        results = [(p['id'], p['product-name'], p['console-name'], p['loose-price'], p['cib-price']) for p in found_prices]
        print results


main_class = VgPriceChartingCommand
