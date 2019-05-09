import math


class VectorDistance:
    @staticmethod
    def calculate(user_classification, menu_classification):
        distance = 0
        classification_used = False
        for column in user_classification:
            if menu_classification is None:
                continue

            menu = getattr(menu_classification, column)
            if menu is not None and user_classification[column] is not None:
                classification_used = True
                distance += (user_classification[column] - menu)

        if not classification_used:
            return None

        return math.fabs(distance)
