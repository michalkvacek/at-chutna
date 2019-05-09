import abc
from elasticsearch_dsl import Index, analyzer, analysis
from elasticsearch import helpers

from classification.elasticsearch.elasticsearch import ElasticsearchWrapper


class BaseElasticSearchLoader:
    def __init__(self):
        es = ElasticsearchWrapper()
        self.client = es.client

    @staticmethod
    def _get_analyzer():
        stopwords = analysis.token_filter(
            'czech_stopwords',
            type="stop",
            stopwords=['_czech_']
        )
        min_length = analysis.token_filter(
            'min_length',
            type="length",
            min=3
        )
        unique = analysis.token_filter(
            'czech_unique',
            type="unique",
            only_on_same_position=True
        )
        stemmer = analysis.token_filter(
            'czech_stemmer',
            type="hunspell",
            locale="cs_CZ"
        )
        remove_accents = analysis.token_filter('icu_folding')
        lowercase = analysis.token_filter('lowercase')

        czech_analyzer = analyzer(
            'czech',
            tokenizer="standard",
            filter=[lowercase, min_length, stopwords, stemmer, remove_accents, unique],
        )

        return czech_analyzer

    def _create_index(self, index_name):
        if self.client.indices.exists(index=index_name):
            return

        czech_analyzer = self._get_analyzer()

        index = Index(name=index_name)
        index.delete(ignore=404)
        index.settings(
            number_of_shards=1,
            number_of_replicas=0
        )

        index.analyzer(czech_analyzer)

        index.create()

    @abc.abstractmethod
    def get_data(self):
        pass

    def load(self):
        helpers.bulk(self.client, self.get_data())
