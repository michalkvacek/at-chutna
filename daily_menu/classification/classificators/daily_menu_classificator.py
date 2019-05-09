from classification.classificators.rules.daily_menu.cousine import CousineClassificator
from classification.classificators.rules.daily_menu.simple_rules import *
from classification.models import DailyMenuClassification
from classification.tagger.rules.simple_rules import Vegetarian, Vegan
from restaurants.models import Cousine


class DailyMenuClassificator:
    classification_rules = [
        ClassificationRule(column='vegetarian', mandatory_tags=[Vegetarian.name]),
        ClassificationRule(column='vegan', mandatory_tags=[Vegan.name]),
        ClassificationRule(column='pork', mandatory_tags=['vepr', 'slanina']),
        ClassificationRule(column='beef', mandatory_tags=['hovezi']),
        ClassificationRule(column='pasta', mandatory_tags=['testovina']),
        ClassificationRule(column='fish', mandatory_tags=['ryba', 'rybi']),
        ClassificationRule(column='poultry', mandatory_tags=['drubez']),
        ClassificationRule(column='seafood', mandatory_tags=['morske']),
        ClassificationRule(column='meat', mandatory_tags=['maso']),
        ClassificationRule(column='mushrooms', mandatory_tags=['houba', 'houbovy']),
        ClassificationRule(column='tofu', mandatory_tags=['tofu']),
        ClassificationRule(column='venison', mandatory_tags=['divocina']),
        ClassificationRule(column='cheese', mandatory_tags=['syr']),
    ]

    def __init__(self):
        cousines = Cousine.objects.prefetch_related('cousinetags_set').all()

        for cousine in cousines:
            self.classification_rules.append(CousineClassificator(cousine=cousine))

    def get_classification_columns(self):
        return [rule.column for rule in self.classification_rules]

    def reset_classification(self, menu):
        if menu.automatic_classification:
            DailyMenuClassification.objects.filter(pk=menu.automatic_classification).delete()

        model = DailyMenuClassification()
        model.save()

        menu.automatic_classification = model
        menu.classification_in_progress = False # classification is assigned, now we need to calculate it
        menu.save()

        return model

    def run_classification(self, menu, tags):
        model = self.reset_classification(menu)

        for rule in self.classification_rules:
            classification = rule.classify(menu, tags)

            if model and classification[0] is not None:
                setattr(model, classification[0], classification[1])

        model.save()
