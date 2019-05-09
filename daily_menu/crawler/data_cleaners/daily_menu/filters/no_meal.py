from difflib import SequenceMatcher

from classification.models import NotMealTags
from classification.tagger.recipe_tagger import RecipeTagger
from crawler.data_cleaners.daily_menu.filters.base_filter import BaseFilter


class NoMealFilter(BaseFilter):
    def __init__(self):
        self.no_meal_tags = []
        self.recipe_tagger = RecipeTagger()

    def _load_no_meal_tags(self):
        if len(self.no_meal_tags) > 0:
            # already loaded
            return

        tags = NotMealTags.objects.filter(is_significant=True).all()
        for tag in tags:
            self.no_meal_tags.append(tag.tag)

        return self.no_meal_tags

    @staticmethod
    def similarity(a, b):
        """
        Computes similarity between two given strings
        :param a:
        :param b:
        :return: bool
        """
        if a in b or b in a:
            return 1

        return SequenceMatcher(None, a, b).ratio()

    def _is_no_meal(self, word):
        for tag in self.no_meal_tags:
            if self.similarity(tag, word) > 0.8:
                return True

        return False

    def filter(self, menus):
        """
        Filter given daily menus - exclude words containing more than 60 % of no-meal tags
        :param menus:
        :return:
        """

        self._load_no_meal_tags()

        filtered = []
        for menu in menus:
            analyzed = self.recipe_tagger.get_static_tags(menu['name'], include_multiple_words=False)

            hits = 0
            for word in analyzed:
                if self._is_no_meal(word):
                    hits += 1

            if len(analyzed) == 0:
                print("len(analyzed) == 0!!!!!!!!!!!!!!")
                print(menu)
                print("--------------------------------")
                hit_ratio = 0
            else:
                hit_ratio = hits / len(analyzed)  # / hits if hits > 0 else 0

            if hit_ratio < 0.4:
                filtered.append(menu)

        return filtered
