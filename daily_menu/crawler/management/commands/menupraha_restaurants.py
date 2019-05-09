import datetime
import re

from crawler.management.commands.helpers.base_scrapper import BaseScrapper
from crawler.models import RestaurantScraperConfig
from crawler.scrapers.beautifulsoup_wrapper import BeautifulSoupWrapper
from crawler.scrapers.restaurant_duplicates_checker import RestaurantDuplicatesChecker
from restaurants.models import Restaurant


class MenuPrahaRestaurantParser():
    def __init__(self, url):
        self.soup = BeautifulSoupWrapper(url)

    def get_name(self):
        text = self.soup.find('h1')

        if text is None:
            return None

        return text.text

    def get_address(self):
        address_wrapper = self.soup.find('h3', itemprop='address')

        if address_wrapper is None:
            return None

        street = address_wrapper.find('span', itemprop='streetAddress').text
        city = address_wrapper.find('span', itemprop='addressLocality').text

        map_link = address_wrapper.find('a')['href']

        gps = re.search(r'([0-9]{1,2}\.[0-9]+,[0-9]{1,2}\.[0-9]+)', map_link)

        if gps is None:
            gps = (None, None)
        else:
            gps = gps.group(1).split(',') if ',' in gps.group(1) else (None, None)

        return {
            "address": street + ", " + city,
            "gps": {
                "lat": float(gps[0]) if gps[0] is not None else None,
                "lng": float(gps[1])if gps[1] is not None else None
            }
        }

    def get_restaurant(self):
        return {
            "name": self.get_name(),
            "locality": self.get_address(),
        }


class Command(BaseScrapper):
    help = 'Scrape recipes websites and save new recipes'

    def handle(self, *args, **kwargs):
        soup = BeautifulSoupWrapper("https://menupraha.cz/sitemap.xml")

        checker = RestaurantDuplicatesChecker()

        urls = [restaurant_url.text for restaurant_url in soup.select('loc')]
        urls = list(filter(lambda x: re.search(r'restaurace/[0-9]+', x), urls))

        for url in urls:
            parser = MenuPrahaRestaurantParser(url)
            details = parser.get_restaurant()

            if details is None:
                continue

            if checker.already_exists(details['name'],
                                      (details['locality']['gps']['lat'], details['locality']['gps']['lng'])):
                print(details['name'] + ' se zda ze existuje')
                continue

            restaurant = Restaurant(
                name=details['name'],
                menu_url=url,
                address=details['locality']['address'],
                gps_lat=details['locality']['gps']['lat'],
                gps_lng=details['locality']['gps']['lng']
            )
            restaurant.save()

            print(details['name'])

            config = RestaurantScraperConfig(
                restaurant=restaurant,
                scraper_parameters=url,
                next_visit=datetime.date.today(),
                next_visit_interval=1,
                menu_scraper='daily_menu.MenuPraha'
            )

            config.save()

            # return
