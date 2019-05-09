from crawler.scrapers.recipes.base_recipe_downloader import SitemapRecipeDownloader
from crawler.scrapers.recipes.parsers.toprecepty_parser import TopReceptyParser


class TopReceptyDownloader(SitemapRecipeDownloader):
    def __init__(self):
        super().__init__()
        self.base_sitemap_url = 'https://www.toprecepty.cz/sitemap.xml'
        self.recipe_sitemap_keyword = 'recept'
        self.parser = TopReceptyParser
