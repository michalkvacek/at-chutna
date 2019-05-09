from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from classification.classificators.user_classificator import UserClassificator

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        users = get_user_model().objects.all()

        classificator = UserClassificator()
        for user in users:
            classificator.run_classification(user)

