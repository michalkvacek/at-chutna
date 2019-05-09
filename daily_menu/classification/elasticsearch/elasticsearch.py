from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
import requests

from config import app


class ElasticsearchWrapper():
    def __init__(self):
        connections.create_connection(hosts=[app.ELASTICSEARCH_HOST], timeout=5)

        self.client = Elasticsearch(app.ELASTICSEARCH_HOST + ":" + str(app.ELASTICSEARCH_PORT))

    def send_raw_query(self, method, url, body):
        if method.lower() == 'get':
            response = requests.get(
                "http://"+app.ELASTICSEARCH_HOST + ":" + str(app.ELASTICSEARCH_PORT) + "/" + url,
                json=body)
        else:
            raise AttributeError('unsupported method!')

        return response
