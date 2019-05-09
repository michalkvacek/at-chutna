from django.utils import timezone

from user.models import UserRecommendationLocation
from user.recommendations.classification_loader import ClassificationLoader
from user.recommendations.loaders.loader import MostSimilarMenuLoader
from user.recommendations.similarity import VectorDistance


class MostSimilarDailyMenu:
    def __init__(self):
        self.distance = VectorDistance()
        self.classification = ClassificationLoader()

    def get_location(self, user, type, location):
        if location is None:
            for l in user.locations.all():
                if l.type == type:
                    location = l

        if location is None:
            # no location for user found, create default
            location = UserRecommendationLocation(user=user, type=type, recommendation_type='restaurants')
            location.save()

        return location

    def get_recommendation_for_user(self, user, max=5, type='personal', location=None):
        classification = self.classification.get_for_user(user)

        location = self.get_location(user, type, location)
        today_menus = MostSimilarMenuLoader(user, classification, location).get_daily_menu()

        recommendations = []
        for menu in today_menus:
            if len(menu.name) < 20:
                continue

            distance = self.distance.calculate(classification, menu.automatic_classification)

            # ignore not classified meals
            if distance is None:
                continue
            elif distance < 5:
                recommendations.append((menu, distance))

        recommendations = sorted(recommendations, key=lambda recommendation: recommendation[1])

        restaurants = set()
        final_recommendations = []
        for recommendation in recommendations:
            restaurant = recommendation[0].restaurant
            if restaurant in restaurants:
                continue

            final_recommendations.append((recommendation[0], []))
            restaurants.add(restaurant)

            if len(final_recommendations) == max:
                break


        return {
            'user_recommendations': final_recommendations,
            'friends_recommendations': []
        }
