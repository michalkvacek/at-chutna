import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import time


class BeautifulSoupWrapper(BeautifulSoup):
    def __init__(self, recipe_url, delay=None):
        if delay is not None:
            time.sleep(delay)

        headers = {"User-Agent": 'AtChutna.cz'}
        resp = requests.get(recipe_url, headers=headers)
        http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)

        self.encoding = html_encoding or http_encoding
        super().__init__(resp.content, 'lxml', from_encoding=self.encoding)
