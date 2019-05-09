import abc
from bs4 import BeautifulSoup
from urllib.request import urlopen


from crawler.data_cleaners.ingredients.cleaner import IngredientsCleaner
from crawler.models import Ingredient, Recipe, RecipeCategory


class BaseRecipeDownloader:
    def __init__(self):
        self.parsed_urls = []
        self.ingredients = {}
        self.categories = {}

        self.downloader = None
        self.ingredients_cleaner = IngredientsCleaner()

    def _init_categories(self):
        """
        Load created categories. These categories are loaded regardless on downloader.
        :return:
        """

        categories = RecipeCategory.objects.all()

        for category in categories:
            self.categories[category.name] = category

    def _init_parsed_urls(self):
        """
        Load already saved recipes, so we will not visit them again
        :return:
        """
        recipes = Recipe.objects.filter(downloaded_by=self.downloader).all()

        for recipe in recipes:
            self.parsed_urls.append(recipe.url)

    def _init_ingredients(self):
        """
        Load ingredient list into memory
        :return:
        """
        ingredients = Ingredient.objects.all()

        for ingredient in ingredients:
            self.ingredients[ingredient.name] = ingredient

    def _create_new_ingredient(self, name):
        """
        Create new ingredient if not found in local database
        :param name:
        :return:
        """
        ingredient = Ingredient(name=name)
        ingredient.save()

        self.ingredients[name] = ingredient

        return ingredient

    def _create_new_category(self, name):
        """
        When category does not exist, create new one
        :param name:
        :return:
        """
        category = RecipeCategory(name=name, downloaded_by=self.downloader)
        category.save()

        self.categories[name] = category

        return category

    def get_ingredient(self, name):
        """
        Get instance of ingredient with given name or create a new one
        :param name:
        :return:
        """

        if not self.ingredients:
            self._init_ingredients()

        ingredient = self.ingredients[name] if name in self.ingredients else self._create_new_ingredient(name)

        return ingredient

    def get_category(self, name):
        """
        Get category from already existing records or create new one
        :param name:
        :return:
        """

        if not self.categories:
            self._init_categories()

        return self.categories[name] if name in self.categories else self._create_new_category(name)

    def _save_recipe(self, recipe_data):
        """
        Save recipe with ingredients and categories (if provided)
        :param recipe_data:
        :return:
        """

        recipe = None
        try:
            recipe = Recipe(
                name=recipe_data['name'],
                url=recipe_data['source'],
                downloaded_by=self.downloader
            )
            recipe.save()
            print(recipe.name)

            recipe_saved = True
        except:
            # recipe did not saved, cannot proceed
            recipe_saved = False

        if recipe is not None and recipe_saved:
            try:
                if 'ingredients' in recipe_data and recipe_data['ingredients']:
                    ingredients = self.ingredients_cleaner.clean(recipe_data['ingredients'])
                    for ingredient in ingredients:
                        recipe.ingredients.add(self.get_ingredient(ingredient))
            except:
                # something didn't fit into database, probably, ignore and continue with another recipe
                pass

            try:
                if 'categories' in recipe_data and recipe_data['categories']:
                    for category in recipe_data['categories']:
                        recipe.categories.add(self.get_category(category))

            except:
                # something didn't fit into database, probably, ignore and continue with another recipe
                pass

        return recipe

    @abc.abstractmethod
    def download(self):
        pass


class SitemapRecipeDownloader(BaseRecipeDownloader):
    def __init__(self):
        super().__init__()
        self.base_sitemap_url = None
        self.recipe_sitemap_keyword = None
        self.parser = None
        self.sitemap_urls = []

    def _load_sitemap_urls(self):
        soup = BeautifulSoup(urlopen(self.base_sitemap_url), "lxml")
        sitemap_urls = soup.find_all('loc')

        for sitemap in sitemap_urls:
            url = sitemap.text

            if self.recipe_sitemap_keyword in url:
                self.sitemap_urls.append(url)

    def download(self):
        self._load_sitemap_urls()
        self._init_parsed_urls()

        for sitemap_url in self.sitemap_urls:
            self._download_recipes_from_sitemap(sitemap_url)

    def _download_recipes_from_sitemap(self, sitemap_url):
        soup = BeautifulSoup(urlopen(sitemap_url), "lxml")
        recipe_urls = soup.find_all('loc')

        for recipe_url in recipe_urls:
            if recipe_url.text in self.parsed_urls:
                continue

            self._download_recipe(recipe_url.text)

    def _download_recipe(self, url):
        parser = self.parser(url)
        recipe_data = parser.parse()

        self._save_recipe(recipe_data)
