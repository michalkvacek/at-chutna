from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Prefetch, Q

from user.models import Recommender, Friendship, Recommendation
from user.recommendations.saver import RecommendationSaver


class Command(BaseCommand):
    help = 'Generate recommendations for users'

    def handle(self, *args, **kwargs):
        # load users
        users = get_user_model().objects.prefetch_related(
            'automatic_classification',
            'manual_classification',
            'locations',
            Prefetch('friends_set', queryset=Friendship.objects.filter(lunch_together=True)),
        ).all()

        saver = RecommendationSaver()
        generators = Recommender.objects.order_by('order').all()

        for generator in generators:
            for user in users:

                print(user.email)

                saver.save_recommendations(generator, user)
