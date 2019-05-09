from collections import Counter
from django.core.management import BaseCommand
from elasticsearch_dsl import Search

from classification.elasticsearch.elasticsearch import ElasticsearchWrapper
from classification.elasticsearch.finders.finders import IngredientsFinder
from classification.elasticsearch.loaders.daily_menu import DailyMenuLoader
from classification.elasticsearch.loaders.ingredients import IngredientsLoader
from classification.elasticsearch.loaders.recipes import RecipesLoader
from classification.elasticsearch.loaders.restaurants import RestaurantsLoader
from crawler.models import Recipe, Ingredient, RecipeCategory


class Command(BaseCommand):
    help = "Update data needed for classification"

    def create_canonical_name_of_ingredients(self):
        ingredients = Ingredient.objects.all()

        finder = IngredientsFinder()
        for ingredient in ingredients:
            tokens = finder.analyze_tokens(ingredient.name)
            ingredient.canonical_name = " ".join(tokens)
            ingredient.save()

    def create_canonical_name_of_categories(self):
        categories = RecipeCategory.objects.all()

        finder = IngredientsFinder()
        for category in categories:
            tokens = finder.analyze_tokens(category.name)

            category.canonical_name = " ".join(tokens)
            category.save()

    def mark_common_ingredients(self):
        """
        Very commong ingredients have no value, we will try to ignore them in classification
        :return:
        """
        recipes = Recipe.objects.prefetch_related('ingredients').all()

        ingredients = Counter()

        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                ingredients[ingredient.canonical_name] += 1

        common_threshold = int(len(ingredients) * 0.03)
        common = ingredients.most_common(common_threshold)

        # todo proverit

        common = list(filter(lambda item: item[1] > 1, common))

        # get only names, not counts
        common = [ingredient[0] for ingredient in common]

        Ingredient.objects.filter(canonical_name__in=common).update(is_common=True)
        Ingredient.objects.exclude(canonical_name__in=common).update(is_common=False)

    def update_search_index(self):
        recipes_loader = RecipesLoader()
        ingredients_loader = IngredientsLoader()
        daily_menu_loader = DailyMenuLoader()
        restaurants_loader = RestaurantsLoader()

        recipes_loader.load()
        ingredients_loader.load()
        daily_menu_loader.load()
        restaurants_loader.load()

    def handle(self, *args, **options):
        self.create_canonical_name_of_ingredients()
        self.create_canonical_name_of_categories()
        self.mark_common_ingredients()
        self.update_search_index()
