
class ClassificationRule:
    column = None
    mandatory_tags = []

    def __init__(self, column=None, mandatory_tags=None):
        if column is not None:
            self.column = column

        if mandatory_tags is not None:
            self.mandatory_tags = mandatory_tags

    def classify(self, model, tags):
        tags_str = "|".join(tags)

        for tag in self.mandatory_tags:
            if tag in tags_str:
                return self.column, 1

        return self.column, None
