from classification.classificators.daily_menu_classificator import DailyMenuClassificator
from restaurants.models import DailyMenu


class UserMenuLoader():
    def __init__(self, user, classification):
        self.constraints = []
        self.classification = classification

    def filter_menus_with_low_classification(self, menus):
        # return menus

        filtered = []

        classification_columns = DailyMenuClassificator().get_classification_columns()

        for menu in menus:
            classifications = 0

            # ignore not-classified menus
            if menu.automatic_classification is None:
                continue

            for column in classification_columns:
                value = getattr(menu.automatic_classification, column)

                if value is not None:
                    classifications += 1

            print(int(len(classification_columns) * 0.2))

            if classifications > int(len(classification_columns) * 0.2):
                filtered.append(menu)

        return filtered

    def filter_by_classification(self, menus):

        filtered = []

        classification_columns = DailyMenuClassificator().get_classification_columns()

        for menu in menus:
            remove = False
            for column in classification_columns:
                value = self.classification[column] if column in self.classification else 0
                menu_value = getattr(menu.automatic_classification, column)

                if menu_value is None:
                    menu_value = 0

                if menu_value > 0 and value < -0.6:
                    remove = True
                    break

            if not remove:
                filtered.append(menu)

        return filtered

    def get_daily_menu(self):
        daily_menu = DailyMenu.objects

        for constraint in self.constraints:
            daily_menu = constraint.filter(daily_menu)

        menus = daily_menu.prefetch_related(
            'dailymenutags_set',
            'restaurant',
            'automatic_classification'
        ).all()

        return self.filter_by_classification(
            self.filter_menus_with_low_classification(
                menus
            )
        )
