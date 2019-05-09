from django.apps import AppConfig

from config import app


class CrawlerConfig(AppConfig):
    name = 'crawler'
    zomato_client_id = app.ZOMATO_CLIENT_ID
