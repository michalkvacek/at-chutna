from crawler.scrapers.recipes.base_recipe_downloader import SitemapRecipeDownloader
from crawler.scrapers.recipes.parsers.recepty_parser import ReceptyParser


class ReceptyDownloader(SitemapRecipeDownloader):
    def __init__(self):
        super().__init__()
        self.base_sitemap_url = 'https://www.recepty.cz/sitemap.xml'
        self.recipe_sitemap_keyword = "recipe"
        self.parser = ReceptyParser

