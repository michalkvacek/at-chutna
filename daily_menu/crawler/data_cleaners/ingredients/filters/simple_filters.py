import abc
import re


class BaseFilter:

    @abc.abstractmethod
    def filter(self, menus):
        pass


class RegexpBasedFilter(BaseFilter):
    patterns = []

    def filter(self, items):
        filtered = []
        for item in items:
            for pattern in self.patterns:
                item = re.sub(pattern, '', item, flags=re.IGNORECASE)

            filtered.append(item)

        return filtered


class RemoveAmountFilter(RegexpBasedFilter):
    patterns = [
        r'[0-9]+\s?g',
        r'[0-9]+\s?ks',
        r'[0-9,.]+\s?kg',
    ]


class DescriptionInBracketsFilter(RegexpBasedFilter):
    patterns = [
        r'\([.*]\)'
    ]


class StripFilter(RegexpBasedFilter):
    patterns = [
        r'^\s',
        r'\s$'
    ]
