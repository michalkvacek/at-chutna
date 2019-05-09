from restaurants.models import CousineTags


class CousineClassificator():
    column = ''

    def __init__(self, cousine):
        self.column = cousine.classification_column
        self._load_tags(cousine)

    def _load_tags(self, cousine):
        tags = list(cousine.cousinetags_set.all())

        self.tags = [tag.tag for tag in tags]

    def classify(self, menu, tags):
        common = list(set(tags) & set(self.tags))

        if len(common) == 0:
            score = 0
        else:
            score=len(common) / len(tags)

        return self.column, score
