import importlib
from django.core.management.base import BaseCommand
from abc import abstractmethod


class BaseScrapper(BaseCommand):
    help = 'Download fresh daily menu of restaurants'

    @staticmethod
    def get_parser_class(submodule, arg = None):
        """
        Creates class instance for given scraper
        :param class_name: class name of created scraper
        :param arg: argument passed to created instance
        :return: MenuParser instance
        """
        class_name = submodule.split('.')[-1]

        module = importlib.import_module('crawler.scrapers.' + submodule.lower())
        class_ = getattr(module, class_name)

        instance = class_(arg) if arg else class_()

        return instance

    @abstractmethod
    def handle(self, *args, **options):
        pass
