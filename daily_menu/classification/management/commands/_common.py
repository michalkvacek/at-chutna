from django.core.management import BaseCommand

from classification.models import NotMeals, NotMealTags
from classification.tagger.recipe_tagger import RecipeTagger
from crawler.models import Recipe, Ingredient


class Command(BaseCommand):
    help = "Find common ingredients"

    def get_tokens(self, menu_name):
        filtered = filter(lambda token: len(token) > 3, menu_name.split(' '))
        transformed = map(lambda token: token.lower(), filtered)
        return list(transformed)

    def handle(self, *args, **options):
        recipes = Recipe.objects.all()[:5000]
        recipe_tagger = RecipeTagger()

        common = {}
        max_distance = 1

        for recipe in recipes:
            start = 0
            # print(recipe.name)
            words = self.get_tokens(recipe.name)

            for i in range(0, len(words)):
                token = recipe_tagger.get_static_tags(words[i], include_multiple_words=False)
                word = " ".join(token)

                if word not in common:
                    common[word] = {}

                start = max(0, i - max_distance)
                end = min(len(words), i + max_distance + 1)

                words_to_examine = words[start:end]

                counter = 0
                weight = 1
                for examined in words_to_examine:
                    tag = recipe_tagger.get_static_tags(examined, include_multiple_words=False)
                    tag_str = " ".join(tag)

                    if tag_str != word:
                        if tag_str not in common[word]:
                            common[word][tag_str] = 0

                        common[word][tag_str] += weight

                    counter += 1

        most_common = {}

        for word in common:
            for second_word in common[word]:
                if common[word][second_word] > 2:

                    if word not in most_common:
                        most_common[word] = []

                    most_common[word].append(second_word)

        print(most_common)
