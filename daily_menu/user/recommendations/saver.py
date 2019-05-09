import importlib
from pprint import pprint

from django.db.models import Count
from django.utils import timezone

from user.models import Recommendation, Recommender, FriendsRecommendation
from user.recommendations.generators.mostsimilardailymenu import MostSimilarDailyMenu


class RecommendationSaver:

    def __init__(self):
        self.friends_recommander = Recommender.objects.filter(recommendation_class='FriendsInvites').first()

    @staticmethod
    def get_recommender_instance(submodule):
        """
        Creates class instance for given scraper
        :param class_name: class name of created scraper
        :param arg: argument passed to created instance
        :return: MenuParser instance
        """
        class_name = submodule.split('.')[-1]

        module = importlib.import_module('user.recommendations.generators.' + submodule.lower())
        class_ = getattr(module, class_name)

        instance = class_()

        return instance

    def save_recommendations(self, generator, user):
        print(generator.name)

        # delete recommendations for today
        if generator != self.friends_recommander:
            Recommendation.objects.filter(
                day=timezone.now().date(),
                user=user,
                recommender=generator
            ).delete()

        recommender = self.get_recommender_instance(generator.recommendation_class)
        recommendations = recommender.get_recommendation_for_user(user)

        # ... and save new ones
        user_recommendations = recommendations['user_recommendations']
        friends_recommendations = recommendations['friends_recommendations']

        for recommendation in user_recommendations:
            menu = recommendation[0]
            friends = recommendation[1]

            recommendation = Recommendation(
                day=timezone.now().date(),
                user=user,
                menu=menu,
                recommender=generator
            )
            recommendation.save()

            # save friends
            for friend in friends:
                FriendsRecommendation(
                    friend=friend,
                    recommendation=recommendation
                ).save()

        if self.friends_recommander is not None and len(friends_recommendations) > 0:
            for recommendations in friends_recommendations:
                for friend in recommendations:
                    for menu in recommendations[friend]:
                        FriendsRecommendation.objects.filter(
                            friend=user,
                            recommendation__user=friend,
                            recommendation__recommender=self.friends_recommander
                        ).delete()

                        Recommendation.objects.filter(
                            day=timezone.now().date(),
                            user=friend,
                            recommender=self.friends_recommander,
                        ).annotate(friends_count=Count('friendsrecommendation')).filter(friends_count=0).delete()


                        recommendation = Recommendation(
                            day=timezone.now().date(),
                            user=friend,
                            menu=menu,
                            recommender=self.friends_recommander
                        )
                        recommendation.save()

                        FriendsRecommendation(
                            friend=user,
                            recommendation=recommendation
                        ).save()
