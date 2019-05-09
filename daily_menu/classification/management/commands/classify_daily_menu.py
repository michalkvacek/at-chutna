from django.core.management import BaseCommand

from classification.classificators.daily_menu_classificator import DailyMenuClassificator
from restaurants.models import DailyMenuTags
from classification.tagger.daily_menu_tagger import DailyMenuTagger
from classification.tagger.not_meals_tagger import NotMealsTagger
from restaurants.models import DailyMenu


class Command(BaseCommand):
    help = "Create canonical form of ingredient names"

    def __init__(self):
        super().__init__()
        self.tagger = DailyMenuTagger()
        self.classifier = DailyMenuClassificator()

    def tag_daily_menu(self, menu):
        tags = self.tagger.get_tags(menu.name)

        # delete all tags which were assigned before
        DailyMenuTags.objects.filter(daily_menu=menu).delete()

        # save new tags
        for tag in tags:
            daily_menu = DailyMenuTags(daily_menu=menu, tag=tag)
            daily_menu.save()

        return tags

    def handle(self, *args, **options):
        # update database of "not meals"
        NotMealsTagger().tag(1)

        first = True
        menus_count = 0
        while first or menus_count > 0:
            first = False
            menus = DailyMenu.objects.filter(
                automatic_classification__isnull=True,
                classification_in_progress=False,
            ).all()[0:300]

            menus_count = menus.count()

            ids = [menu.id for menu in menus]
            query = DailyMenu.objects.filter(pk__in=ids)
            query.update(classification_in_progress=True)

            for menu in menus:
                tags = self.tag_daily_menu(menu)
                self.classifier.run_classification(menu, tags)

