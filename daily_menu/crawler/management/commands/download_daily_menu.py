from datetime import timedelta, datetime

from classification.tagger.not_meals_tagger import NotMealsTagger
from crawler.management.commands.helpers.base_scrapper import BaseScrapper
from crawler.models import RestaurantScraperConfig
from restaurants.models import DailyMenu
from crawler.data_cleaners.daily_menu.cleaner import DailyMenuCleaner


class Command(BaseScrapper):
    help = 'Download fresh daily menu of restaurants'

    def handle(self, *args, **kwargs):
        """
        Selects restaurants marked for data refresh and downloads new daily menu
        :param args:
        :param kwargs:
        :return:
        """
        cleaner = DailyMenuCleaner()
        restaurants = RestaurantScraperConfig.objects.prefetch_related('restaurant').filter(
            active=True,
            next_visit__lte=datetime.now()
        ).all()

        for restaurant_config in restaurants:
            scraper = self.get_parser_class(restaurant_config.menu_scraper, restaurant_config.scraper_parameters)

            print(restaurant_config.scraper_parameters)
            daily_menus = scraper.get_menu()
            daily_menus = cleaner.clean(daily_menus)

            daily_menus_downloaded = 0
            for day in daily_menus:
                # delete daily menus for current day
                DailyMenu.objects.filter(day=day, restaurant=restaurant_config.restaurant).delete()

                for meal in daily_menus[day]:

                    print(meal['name'] + ": " + str(meal['price']))

                    try:
                        restaurant = restaurant_config.restaurant

                        daily_menu = DailyMenu(
                            name=meal['name'],
                            price=meal['price'],
                            day=day,
                            cousine=restaurant.cousine,
                            cousine_set=restaurant.cousine is not None,
                            restaurant=restaurant
                        )
                        daily_menu.save()
                        daily_menus_downloaded += 1

                    except Exception as error:
                        print("Restaurace: " + restaurant_config.restaurant.name)
                        print("Menu: " + meal['name'])
                        print("Chyba: " + str(error))
                        pass

            today = datetime.now().date()

            if restaurant_config.last_successful_download is None:
                restaurant_config.last_successful_download = today

            # plan next visit
            if daily_menus_downloaded > 0:
                restaurant_config.last_successful_download = today
                restaurant_config.next_visit_interval = 1

                last_success_diff = 0
            else:
                if today.weekday() < 5:
                    restaurant_config.next_visit += timedelta(days=restaurant_config.next_visit_interval * 2)
                    restaurant_config.next_visit_interval *= 2

                last_success_diff = (restaurant_config.last_successful_download - today).days

            restaurant_config.active = last_success_diff < 5
            restaurant_config.next_visit += timedelta(days=restaurant_config.next_visit_interval)
            restaurant_config.save()
