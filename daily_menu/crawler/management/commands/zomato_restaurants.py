from django.utils.datetime_safe import datetime
from pyzomato import Pyzomato

from crawler.apps import CrawlerConfig
from crawler.management.commands.helpers.base_scrapper import BaseScrapper
from crawler.models import RecipeIngredientCrawler, RestaurantScraperConfig
from crawler.scrapers.restaurant_duplicates_checker import RestaurantDuplicatesChecker
from restaurants.models import Restaurant


class Command(BaseScrapper):
    help = 'Find restaurants with daily menu'

    def handle(self, *args, **kwargs):
        zomato = Pyzomato(CrawlerConfig.zomato_client_id)

        start = 0
        per_page = 20
        limit = 100  # zomato offers only 100 restaurants ... :(

        checker = RestaurantDuplicatesChecker()

        while start <= limit - per_page:
            results = zomato.search(entity_id=84, category=[7], start=start, count=per_page, sort='rating',
                                    entity_type='city')

            zomato_configurations = RestaurantScraperConfig.objects.filter(menu_scraper='daily_menu.Zomato').all()

            loaded_restaurants = {}
            for config in zomato_configurations:
                loaded_restaurants[config.scraper_parameters] = config

            print("Nalezeno: " + str(len(results['restaurants'])))
            for result in results['restaurants']:
                restaurant = result['restaurant']

                if checker.already_exists(
                        restaurant['name'],
                        (restaurant['location']['latitude'], restaurant['location']['longitude'])
                ):
                    continue

                if restaurant['id'] in loaded_restaurants:
                    local_restaurant = loaded_restaurants[restaurant['id']]
                    # this restaurant is already in our database, update information
                    model = Restaurant.objects.get(pk=local_restaurant.restaurant_id)
                else:
                    model = Restaurant()
                    model.save()
                    RestaurantScraperConfig(
                        menu_scraper='daily_menu.Zomato',
                        restaurant=model,
                        next_visit=datetime.today(),
                        scraper_parameters=restaurant['id']).save()

                model.name = restaurant['name']
                model.menu_url = restaurant['menu_url']
                model.address = restaurant['location']['address']
                model.gps_lat = restaurant['location']['latitude']
                model.gps_lng = restaurant['location']['longitude']
                model.save()

            start += per_page
