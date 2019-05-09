from django.db.models import Prefetch
from elasticsearch_dsl import Document, Keyword, Text

from classification.elasticsearch.loaders.base_loader import BaseElasticSearchLoader
import crawler.models


class Recipe(Document):
    name = Text(analyzer="czech")
    ingredients = Keyword()
    categories = Keyword()

    class Index:
        name = "recipes"


class RecipesLoader(BaseElasticSearchLoader):
    def __init__(self):
        super().__init__()

        self._create_index("recipes")
        Recipe.init()

    def get_data(self):
        recipes = crawler.models.Recipe.objects.prefetch_related(
            Prefetch(
                'ingredients',
                queryset=crawler.models.Ingredient.objects.filter(is_common=False, is_significant=True)
            ),
            Prefetch('categories', queryset=crawler.models.RecipeCategory.objects.filter(is_significant=True))
        ).all()
        for recipe in recipes:
            ingredients = [ingredient.canonical_name for ingredient in recipe.ingredients.all()]
            categories = [ingredient.canonical_name for ingredient in recipe.categories.all()]

            yield Recipe(
                _id=recipe.id,
                name=recipe.name,
                ingredients=ingredients,
                categories=categories,
            ).to_dict(True)
