from datetime import date

from crawler.scrapers.beautifulsoup_wrapper import BeautifulSoupWrapper
from crawler.scrapers.daily_menu.menu_parser import MenuParser


class MenuPraha(MenuParser):
    """Stahovani menu z menupraha.cz"""

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.soup = BeautifulSoupWrapper(self.url)

    def get_name(self):
        return self.soup.find('h1').text

    def get_menu(self):
        menu = self.soup.select('.menu tr')

        today = date.today().isoformat()
        parsed_menus = {
            today: []
        }

        for daily_menu in menu:
            cells = daily_menu.findAll('td')

            if len(cells) != 2:
                continue


            menu_name = cells[0].text.strip()
            price = cells[1].text.strip()

            parsed_menus[today].append({
                "name": menu_name,
                "price": price
            })

        return parsed_menus
