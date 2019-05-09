import re

from crawler.data_cleaners.daily_menu.filters.base_filter import BaseFilter


class PriceExtractor(BaseFilter):
    price_patterns = [
        r"(?i)([0-9]{2,3}\s?Kč)",
        r"(?i)([0-9]{2,3}\s?Kc)",
        r"(?i)(Kč.?\s?[0-9]{2,3})",
        r"(?i)(Kc.?\s?[0-9]{2,3})",
        r"(?i)([0-9]{2,3}\s?,-)",
    ]

    def filter(self, menus):
        """
        Extract price from menu name, only if price was not set
        :param menus:
        :return:
        """

        filtered = []

        for menu in menus:
            if menu['price'] == '':
                menu['price'] = None

            menu['name'] = re.sub(r'(?i)cena', '', menu['name'])

            for pattern in self.price_patterns:
                matches = re.findall(pattern, menu['name'])
                if len(matches) > 0:
                    menu['name'] = re.sub(pattern, "", menu['name'])

                    if not menu['price']:
                        menu['price'] = matches[0]

            if menu['price'] is not None:
                menu['price'] = int(re.sub(r'[^0-9]', '', menu['price']))

                # some restaurants uses field for price as field for phone number, so...
                if menu['price'] > 1000:
                    menu['price'] = None

            filtered.append(menu)

        return filtered
