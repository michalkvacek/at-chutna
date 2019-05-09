import abc
import re


class BaseFilter:

    @abc.abstractmethod
    def filter(self, menus):
        pass


class RegexpBasedFilter(BaseFilter):
    patterns = []

    def filter(self, menus):
        filtered = []
        for menu in menus:
            for pattern in self.patterns:
                menu['name'] = re.sub(pattern, '', menu['name'], flags=re.IGNORECASE)

            filtered.append(menu)

        return filtered
