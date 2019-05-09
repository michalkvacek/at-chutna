from crawler.scrapers.beautifulsoup_wrapper import BeautifulSoupWrapper


class BaseRecipeParser:
    crawler_delay = 0

    def __init__(self, recipe_url):
        self.recipe_url = recipe_url

        self.soup = BeautifulSoupWrapper(recipe_url, delay=self.crawler_delay)

