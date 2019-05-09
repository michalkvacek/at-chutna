from datetime import timedelta

from django.utils import timezone

from classification.classificators.daily_menu_classificator import DailyMenuClassificator
from classification.models import DailyMenuClassification, UserClassification
from restaurants.models import DailyMenu


class UserClassificator:
    def reset_classification(self, user):
        if user.automatic_classification is not None:
            UserClassification.objects.filter(pk=user.automatic_classification.id).delete()

        model = UserClassification()
        model.save()

        user.automatic_classification = model
        user.save()

        return model

    def _count_classifications(self, classifications):
        classifications_counted = {}
        for classification in classifications:
            for field in DailyMenuClassificator().get_classification_columns():
                if field not in classifications_counted:
                    classifications_counted[field] = 0

                if classification is not None:
                    value = getattr(classification, field)
                    classifications_counted[field] += value if value is not None else 0

        return classifications_counted

    @staticmethod
    def _get_daily_menu_classifications(user, liked):
        ids = user.dailymenurating_set.filter(liked=liked).exclude(is_meal=False).all().values_list('daily_menu')

        menus = DailyMenu.objects.prefetch_related(
            'automatic_classification'
        ).filter(
            pk__in=ids,
            day__gte=timezone.now().date() - timedelta(days=30)
        ).all()

        return [menu.automatic_classification for menu in menus]

    def run_classification(self, user):
        model = self.reset_classification(user)

        classifications = self._get_daily_menu_classifications(user, liked=True)
        classifications_disliked = self._get_daily_menu_classifications(user, liked=False)

        liked = self._count_classifications(classifications)
        disliked = self._count_classifications(classifications_disliked)
        classifications_count = len(liked) + len(disliked)

        if classifications_count > 0:
            for field in DailyMenuClassificator().get_classification_columns():
                menus_liked = liked[field] if field in liked else 0
                menus_disliked = disliked[field] if field in disliked else 0

                setattr(model, field, (menus_liked - menus_disliked) / classifications_count)

            model.save()
