import abc


class BaseConstraint:
    def __init__(self, user, classification):
        self.user = user
        self.classification = classification

    @abc.abstractmethod
    def filter(self, query):
        return query