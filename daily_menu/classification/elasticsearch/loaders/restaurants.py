from elasticsearch_dsl import Text, Keyword, Document, Date, Integer

from classification.elasticsearch.loaders.base_loader import BaseElasticSearchLoader
from restaurants.models import DailyMenu, Restaurant


class RestaurantIndex(Document):
    name = Text(analyzer="czech")
    id = Integer()

    class Index:
        name = "restaurants"


class RestaurantsLoader(BaseElasticSearchLoader):
    def __init__(self):
        super().__init__()

        self._create_index("restaurants")
        RestaurantIndex.init()

    def get_data(self):
        restaurants = Restaurant.objects.all()

        for restaurant in restaurants:
            yield RestaurantIndex(
                _id=restaurant.id,
                id=restaurant.id,
                name=restaurant.name,

            ).to_dict(True)
