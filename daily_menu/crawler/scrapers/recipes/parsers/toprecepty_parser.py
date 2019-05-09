from crawler.scrapers.recipes.parsers.base_recipe_parser import BaseRecipeParser


class TopReceptyParser(BaseRecipeParser):

    def get_recipe_name(self):
        return self.soup.select_one('.box-recipe__title').text

    def get_recipe_ingredients(self):
        ingredient_boxes = self.soup.select('#ingredients-list')

        ingredients = []
        if ingredient_boxes:
            for box in ingredient_boxes:
                rows = box.find_all('dt')
                for ingredient in rows:
                    ingredients.append(ingredient.text)

        return ingredients

    def get_recipe_categories(self):
        category_boxes = self.soup.select('.box-info__item--kategorie')

        categories = []
        for box in category_boxes:
            category_links = box.find_all('a')

            for link in category_links:
                categories.append(link.text)

        return categories

    def parse(self):
        return {
            'name': self.get_recipe_name(),
            'source': self.recipe_url,
            'categories': self.get_recipe_categories(),
            'ingredients': self.get_recipe_ingredients(),
        }
