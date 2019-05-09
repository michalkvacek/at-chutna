from elasticsearch_dsl import Search, Q

from classification.elasticsearch.finders.base_finder import BaseFinder


class IngredientsFinder(BaseFinder):

    def __init__(self):
        super().__init__()
        self.index = 'ingredients'


class RecipesFinder(BaseFinder):

    def __init__(self):
        super().__init__()
        self.index = 'recipes'

    def find(self, recipe_name):
        # print(recipe_name)
        hits = Search(using=self.client).index(self.index).query(
            'multi_match',
            fields=['name'],
            query=recipe_name,
            fuzziness=1,
            minimum_should_match="2<75%"
        )
        hits.execute()

        # we will accept recipe names not longer than 200 % of original recipe name
        hit_max_length = int(len(recipe_name) * 2)
        hit_min_length = int(len(recipe_name) * 0.5)
        recipes = []

        for hit in hits:
            if hit_min_length > len(hit.name) or len(hit.name) > hit_max_length:
                continue

            recipe = {
                "name": hit.name,
                "ingredients": [],
                "tags": [],
                "categories": []
            }

            has_extra_info = False
            if hasattr(hit, 'categories'):
                recipe['categories'] = [category for category in hit.categories]
                if len(recipe['categories']) > 0:
                    has_extra_info = True

            if hasattr(hit, 'ingredients'):
                recipe['ingredients'] = [ingredient for ingredient in hit.ingredients]
                if len(recipe['ingredients']) > 0:
                    has_extra_info = True

            if hasattr(hit, 'tags'):
                recipe['tags'] = [tag for tag in hit.tags]
                if len(recipe['tags']) > 0:
                    has_extra_info = True

            # append only if recipe has something more then just name
            if has_extra_info:
                recipes.append(recipe)

        return recipes


class DailyMenuFinder(RecipesFinder):

    def __init__(self):
        super().__init__()
        self.index = 'daily_menu'
