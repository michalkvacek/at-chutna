from django.utils import timezone

from crawler.management.commands.helpers.base_scrapper import BaseScrapper
from crawler.models import RecipeIngredientCrawler


class Command(BaseScrapper):
    help = 'Scrape recipes websites and save new recipes'

    def handle(self, *args, **kwargs):
        crawlers = RecipeIngredientCrawler.objects.filter(next_visit__lte=timezone.now()).all()

        for crawler in crawlers:
            print(crawler.crawler_class)
            scrapper = self.get_parser_class(crawler.crawler_class)
            scrapper.downloader = crawler
            scrapper.download()
