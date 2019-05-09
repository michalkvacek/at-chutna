from pyzomato import Pyzomato

from crawler.scrapers.daily_menu.menu_parser import MenuParser
from crawler.apps import CrawlerConfig


class Zomato(MenuParser):
    def __init__(self, restaurant_id):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.zomato = Pyzomato(CrawlerConfig.zomato_client_id)

    def get_menu(self):
        info = self.zomato.getDailyMenu(self.restaurant_id)

        if 'daily_menus' not in info or len(info['daily_menus']) == 0:
            return {}

        date = self._get_date(info['daily_menus'][0]['daily_menu']['start_date'])

        parsed_menus = {date: []}
        for dish in info['daily_menus'][0]['daily_menu']['dishes']:
            parsed_menus[date].append({
                "name": dish['dish']['name'],
                "price": dish['dish']['price']
            })

        return parsed_menus
