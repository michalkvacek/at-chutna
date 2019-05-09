from collections import Counter
from django.core.management import BaseCommand

from classification.tagger.daily_menu_tagger import DailyMenuTagger
from classification.tagger.rules.simple_rules import Vegetarian, Vegan
from restaurants.models import CousineTags, Cousine
from restaurants.models import DailyMenu, Restaurant







class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        # tagger = CousineTagger()
        # tagger.save()
        american = Cousine.objects.filter(pk=3).first()

        classification = CousineClassificator(american)


        test = DailyMenu.objects.exclude(automatic_classification__isnull=True).filter(name__icontains="burger").all()
        for recipe in test:

            tags = list(recipe.dailymenutags_set.values_list('tag', flat=True))

            score = classification.classify(recipe, tags)
            print(recipe.name+": "+str(score))

        # print(common)
