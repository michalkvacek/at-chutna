from elasticsearch_dsl import Document, Text

from classification.elasticsearch.loaders.base_loader import BaseElasticSearchLoader
import crawler.models


class Ingredient(Document):
    name = Text(analyzer="czech")

    class Index:
        name = "ingredients"


class IngredientsLoader(BaseElasticSearchLoader):
    def __init__(self):
        super().__init__()

        self._create_index("ingredients")
        Ingredient.init()

    def get_data(self):
        for ingredient in crawler.models.Ingredient.objects.filter(is_common=False).all():
            yield Ingredient(_id=ingredient.id, name=ingredient.name).to_dict(True)
