import re

from classification.models import NotMealTags
from classification.tagger.recipe_tagger import RecipeTagger
from crawler.data_cleaners.daily_menu.filters.base_filter import BaseFilter, RegexpBasedFilter


class MinimumLengthFilter(BaseFilter):
    """
    Remove menu names shorter than given limit
    """

    def __init__(self, min_length_limit=10):
        self.length_limit = min_length_limit

    def filter(self, menus):
        filtered = []

        for menu in menus:
            name = menu['name'].strip(" ")
            if len(name) >= self.length_limit:
                filtered.append(menu)

        return filtered


class LinesFilter(RegexpBasedFilter):
    """
    Remove three and more consecutive chars (lines etc.)
    """

    patterns = [
        r'(\S)\1{3,}'
    ]


class RemoveDuplicates(BaseFilter):

    def filter(self, menus):
        existing = set()

        filtered = []

        for menu in menus:
            if menu['name'] not in existing:
                filtered.append(menu)
                existing.add(menu['name'])

        return filtered


class MenuNameTrimmer(BaseFilter):
    """
    Remove trailing space
    """

    badchars = ' ,.(_-='

    def trim_name(self, name):
        run = True
        string_len = len(name)
        while run:
            for char in self.badchars:
                name = name.strip(char)

            run = len(name) < string_len
            string_len = len(name)

        return name

    def filter(self, menus):
        filtered = []
        for menu in menus:
            menu['name'] = self.trim_name(menu['name'])
            filtered.append(menu)

        return filtered
