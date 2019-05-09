from user.recommendations.constraints.location import LocationConstraint
from user.recommendations.constraints.simple_constraints import TodayMenus
from user.recommendations.loaders.base import UserMenuLoader


class MostSimilarMenuLoader(UserMenuLoader):
    def __init__(self, user, classification, recommendation_location):
        super().__init__(user, classification)

        self.constraints = [
            TodayMenus(user, self.classification),
            LocationConstraint(user, self.classification, recommendation_location),
            # Vegetarian(user, self.classification),
            # Vegan(user, self.classification)
        ]

