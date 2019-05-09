from elasticsearch_dsl import Text, Keyword, Document, Date, Integer

from classification.elasticsearch.loaders.base_loader import BaseElasticSearchLoader
from restaurants.models import DailyMenu


class DailyMenuIndex(Document):
    name = Text(analyzer="czech")
    tags = Keyword()
    id = Integer()
    day = Date()

    class Index:
        name = "daily_menu"


class DailyMenuLoader(BaseElasticSearchLoader):
    def __init__(self):
        super().__init__()

        self._create_index("daily_menu")
        DailyMenuIndex.init()

    def get_data(self):
        recipes = DailyMenu.objects.prefetch_related(
            'dailymenutags_set'
        ).filter(
            automatic_classification__isnull=False
        ).all()

        for recipe in recipes:
            tags = [tag.tag for tag in recipe.dailymenutags_set.all()]

            yield DailyMenuIndex(
                _id=recipe.id,
                id=recipe.id,
                name=recipe.name,
                tags=tags,
                day=recipe.day
            ).to_dict(True)
