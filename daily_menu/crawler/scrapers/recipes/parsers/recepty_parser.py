from crawler.scrapers.recipes.parsers.base_recipe_parser import BaseRecipeParser


class ReceptyParser(BaseRecipeParser):
    def __recipe_categories(self, keyword):
        elements = self.soup.select('.recipe-categories__detail-categories')
        categories = None

        for element in elements:
            if keyword in element.text.lower():
                categories = element.find_all('a')
                break

        if categories:
            categories = [category.text for category in categories]

        return categories

    def get_recipe_name(self):
        return self.soup.select_one('.recipe-title__title').text

    def get_recipe_ingredients(self):
        return self.__recipe_categories('ingredience')

    def get_recipe_categories(self):
        return self.__recipe_categories('kategorie')

    def parse(self):
        return {
            'name': self.get_recipe_name(),
            'source': self.recipe_url,
            'ingredients': self.get_recipe_ingredients(),
            'categories': self.get_recipe_categories()
        }
