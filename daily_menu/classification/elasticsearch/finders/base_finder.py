from classification.elasticsearch.elasticsearch import ElasticsearchWrapper


class BaseFinder():
    def __init__(self):
        self.es = ElasticsearchWrapper()
        self.client = self.es.client
        self.index = ''

    def analyze_tokens(self, text):
        response = self.es.send_raw_query('GET', self.index + '/_analyze', {
            "analyzer": "czech",
            "text": text
        })
        data = response.json()

        tokens = []
        expected_position = 0
        for token in data['tokens']:
            # accept only first word on given position
            if token['position'] >= expected_position:
                tokens.append(token['token'])
                expected_position += 1

        tokens.sort()

        return tokens
