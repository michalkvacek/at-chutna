from classification.classificators.daily_menu_classificator import DailyMenuClassificator


class ClassificationLoader():

    def __init__(self):
        self.rules= DailyMenuClassificator().get_classification_columns()

    def get_for_user(self, user):
        auto_classification = user.automatic_classification
        manual_classification = user.manual_classification
        classification = {}
        for rule in self.rules:

            has_classification = auto_classification is not None or manual_classification is not None

            if has_classification:
                if auto_classification is not None and getattr(auto_classification, rule) is not None:
                    has_classification = getattr(auto_classification, rule) is not None

                if manual_classification is not None and getattr(manual_classification, rule) is not None:
                    has_classification = getattr(manual_classification, rule) is not None

            if not has_classification:
                # nothing to do, this column will be ignored...
                classification[rule] = None
                continue

            classification[rule] = 0

            if auto_classification is not None:
                value = getattr(auto_classification, rule)
                classification[rule] += float(value) if value is not None else 0

            if manual_classification is not None:
                value = getattr(manual_classification, rule)
                classification[rule] += float(value) if value is not None else 0

        # normalize vectors
        for rule in classification:
            if classification[rule] is not None:
                classification[rule] = min(1, classification[rule]) if classification[rule] > 0 else max(-1, classification[rule])

        return classification
