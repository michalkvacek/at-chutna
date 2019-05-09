from crawler.data_cleaners.ingredients.filters.simple_filters import RemoveAmountFilter, DescriptionInBracketsFilter, \
    StripFilter


class IngredientsCleaner:
    def __init__(self):
        self.filters = [
            RemoveAmountFilter(),
            DescriptionInBracketsFilter(),
            StripFilter(),
        ]

    def clean(self, data):
        cleaned_output = []

        for ingredient in data:
            clean_ingredient = ingredient
            for filter in self.filters:
                clean_ingredient = filter.filter(clean_ingredient)

        return cleaned_output
