from crawler.data_cleaners.daily_menu.filters.base_filter import BaseFilter


class SplittedMenuName(BaseFilter):
    def filter(self, menus):

        filtered = []

        price = None
        menu_name = ''

        # ignore menus written all in lower/upper case
        using_uppercase = False
        using_lowercase = False
        for menu in menus:
            if not menu['name'].islower():
                using_lowercase = True

            if not menu['name'].isupper():
                using_uppercase = True

            if using_lowercase and using_uppercase:
                break

        # these menus are not using uppercased letters
        # we are not able to determine start and end of the menu name -> give up
        if not using_uppercase or not using_lowercase:
            return menus

        for menu in menus:
            first_letter = menu['name'].strip(" ")[0]
            if first_letter.isupper() or not first_letter.isalpha():
                if menu_name != '':
                    filtered.append({
                        'name': menu_name,
                        'price': price
                    })
                    price = None

                menu_name = menu['name']
            else:
                menu_name += " " + menu['name']

            if menu['price'] is not None and menu['price'] > 0:
                price = menu['price']

        if len(menu_name) > 0:
            filtered.append({
                'name': menu_name,
                'price': price
            })

        return filtered
