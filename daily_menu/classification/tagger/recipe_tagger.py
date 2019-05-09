from collections import Counter
from itertools import takewhile

from classification.elasticsearch.finders.finders import RecipesFinder, DailyMenuFinder
from classification.tagger.static_tagger import StaticTagger


class RecipeTagger:
    most_common_tags_percentage = 0.3
    recipe_finder = RecipesFinder()
    static_tagger = StaticTagger()
    daily_menu_finder = DailyMenuFinder()

    def get_static_tags(self, menu_name, include_separate_words=True, include_multiple_words=True):
        all_tags = set()

        parts = self.static_tagger.get_tags(menu_name)
        for part in parts:
            tokens = self.recipe_finder.analyze_tokens(part)
            if len(tokens) > 0:
                if include_multiple_words:
                    all_tags.add(" ".join(tokens))

                if include_separate_words:
                    all_tags.update(tokens)

        return all_tags

    @staticmethod
    def _count_keywords(recipes):
        items = Counter()

        for keyword in ['ingredients', 'tags', 'categories']:

            # count weight

            weight = 0
            for recipe in recipes:
                if keyword in recipe and len(recipe[keyword]) > 0:
                    weight += 1

            if weight == 0:
                continue

            weight = int(len(recipes) / weight)

            for recipe in recipes:
                if keyword in recipe:

                    # apply weight
                    for i in range(0, weight):
                        items.update(recipe[keyword])

        return items

    @staticmethod
    def _filter_by_frequency(tags: Counter, min_frequency):
        data = tags.most_common()

        try:
            val = data[min_frequency - 1][1]
        except IndexError as e:
            return []

        return list(takewhile(lambda x: x[1] >= val, data))

    def get_tags_from_recipes(self, recipes):
        tags = self._count_keywords(recipes)

        if len(tags) == 0:
            return []

        min_frequency = max(1, int(len(tags) * self.most_common_tags_percentage))
        counted_tags = self._filter_by_frequency(tags, min_frequency)

        return [tag[0] for tag in counted_tags]

    def get_tags(self, menu_name, tags=None):
        recipes = self.recipe_finder.find(menu_name)
        daily_menus = self.daily_menu_finder.find(menu_name)

        recipes = recipes + daily_menus

        all_tags = set()
        if len(recipes) > 0:
            extra_tags = self.get_tags_from_recipes(recipes)
            all_tags.update(extra_tags)

        return all_tags


class TagExpander(RecipeTagger):
    most_common_tags_percentage = 0.1

    def get_tags(self, menu_name, tags=None):
        if tags is None:
            tags = []

        extra_tags = set()
        for tag in tags:
            if " " in tag:
                # print(tag)
                recipes = self.recipe_finder.find(tag)

                extra_tags.update(self.get_tags_from_recipes(recipes))

        return extra_tags
