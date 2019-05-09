from user.recommendations.constraints.base_constraint import BaseConstraint


class Vegetarian(BaseConstraint):
    threshold = 0.9

    def is_user_vegetarian(self):
        if self.classification['vegetarian'] is None:
            return False

        return self.classification['vegetarian'] > self.threshold and self.classification['meat'] < (1 - self.threshold)

    def filter(self, query):
        if self.is_user_vegetarian():
            return query.filter(automatic_classification__vegetarian=1)
        else:
            return query
