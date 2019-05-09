from datetime import timedelta
import dateparser
from django.utils import timezone

from crawler.data_cleaners.daily_menu.filters.base_filter import BaseFilter
from crawler.data_cleaners.daily_menu.filters.no_meal import NoMealFilter
from crawler.data_cleaners.daily_menu.filters.simple_filters import MinimumLengthFilter, MenuNameTrimmer, LinesFilter, \
    RemoveDuplicates
from crawler.data_cleaners.daily_menu.filters.price_extractor import PriceExtractor
from crawler.data_cleaners.daily_menu.filters.splitted_menu_name import SplittedMenuName


class DailyMenuCleaner:
    def __init__(self):

        self.filters = [
            MinimumLengthFilter(5),
            PriceExtractor(),
            SplittedMenuName(),
            NoMealFilter(),
            MenuNameTrimmer(),
            LinesFilter(),
            MinimumLengthFilter(5),
            RemoveDuplicates()
        ]

        today = timezone.now().date()
        self.start = today - timedelta(days=today.weekday())

    def get_clean_date(self, day):
        day_number = dateparser.parse(day).weekday()
        menu_day = self.start + timedelta(days=day_number)

        return menu_day

    def clean_daily_menu(self, menu):
        """
        Iterate over menus from one day, run filters and clean data
        :param menu:
        :return:
        """

        clean_menu = menu

        for filter in self.filters:
            clean_menu = filter.filter(clean_menu)

        return clean_menu[:50]

    def clean(self, data):
        """
        Iterate over days and run filter on all daily menus
        :param data:
        :return:
        """

        cleaned_output = {}

        for day in data:
            cleaned_output[self.get_clean_date(day)] = self.clean_daily_menu(data[day])

        return cleaned_output
