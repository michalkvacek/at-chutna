from collections import Counter

from classification.models import NotMealTags
from classification.tagger.recipe_tagger import RecipeTagger
from user.models import DailyMenuRating


class NotMealsTagger:
    @staticmethod
    def get_not_meals():
        """
        Load all "not meal" ratings and count occurences
        :return:
        """

        not_meals = DailyMenuRating.objects.filter(is_meal=False).prefetch_related('daily_menu').all()
        tagger = RecipeTagger()

        tags_counted = Counter()
        for rating in not_meals:
            tags = tagger.get_static_tags(rating.daily_menu.name, include_multiple_words=False)

            for tag in tags:
                tags_counted[tag] += 1

        return tags_counted

    @staticmethod
    def save_not_meals_tags(tags_counted: Counter, tag_min_count):
        NotMealTags.objects.all().delete()

        count = len(tags_counted)
        for tag in tags_counted.most_common():
            if tag[1] >= tag_min_count:
                NotMealTags(tag=tag[0], is_significant=True, frequency=tag[1] / count).save()

    def tag(self, threshold=1):
        tags = self.get_not_meals()
        self.save_not_meals_tags(tags, threshold)
