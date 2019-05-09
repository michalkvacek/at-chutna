from user.recommendations.constraints.base_constraint import BaseConstraint


class Vegan(BaseConstraint):
    threshold = 0.95

    def is_user_vegan(self):
        if self.classification['vegan'] is None:
            return False

        return self.classification['vegan'] > self.threshold

    def filter(self, query):
        if self.is_user_vegan():
            return query.filter(automatic_classification__vegan=1)
        else:
            return query
