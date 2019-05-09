from collections import Counter

from classification.tagger.daily_menu_tagger import DailyMenuTagger
from restaurants.models import DailyMenu, CousineTags
from classification.tagger.rules.simple_rules import Vegetarian, Vegan


class CousineTagger():
    tagger = DailyMenuTagger()

    def _load_tags(self):
        menus = DailyMenu.objects.prefetch_related('cousine').exclude(cousine__isnull=True).all()

        ignored_tags = [Vegan.name, Vegetarian.name]

        cousine_tags = {}
        for recipe in menus:

            cousine = recipe.cousine

            if cousine not in cousine_tags:
                cousine_tags[cousine] = Counter()

            tags = self.tagger.get_tags(recipe.name)
            for tag in tags:
                if tag in ignored_tags:
                    continue

                cousine_tags[cousine][tag] += 1

        return cousine_tags

    def save(self):
        cousine_tags = self._load_tags()

        for cousine in cousine_tags:
            most_common = {k: v for k, v in cousine_tags[cousine].items() if v > 3}
            CousineTags.objects.filter(cousine=cousine).delete()

            for tag in most_common:
                CousineTags(cousine=cousine, tag=tag).save()
