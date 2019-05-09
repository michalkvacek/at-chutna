from django.test import TestCase

from crawler.data_cleaners.daily_menu.cleaner import DailyMenuCleaner


class TestDataCleaner(TestCase):

    def setUp(self):
        self.cleaner = DailyMenuCleaner()

    def test_minimum_length(self):
        menus = [{"name": "MENU", "price": ""}]
        cleaned = self.cleaner.clean_daily_menu(menus)
        self.assertEqual(0, len(cleaned))

    def test_price_extractor(self):
        menus = [
            {"name": "Polední menu 1, 45 Kč", "price": ""},
            {"name": "Polední menu 2, Kc 45", "price": ""},
            {"name": "Polední menu 3, 45 Kc", "price": ""},
            {"name": "Polední menu 4, KČ: 45", "price": ""},
            {"name": "Polední menu 5, kc 45", "price": ""},
            {"name": "Polední menu 6, cena 45 kc", "price": ""},
            {"name": "Polední menu 7, cena: 45 kč", "price": ""},
        ]

        cleaned = self.cleaner.clean_daily_menu(menus)

        self.assertEquals(len(menus), len(cleaned))

        for menu in cleaned:
            self.assertEqual(menu['price'], 45)

    def test_phone_in_price(self):
        menus = [
            {"name": "Rozvoz poledního menu 1, tel:", "price": "+420 123 456 748"},
            {"name": "Rozvoz poledního menu 2, tel:", "price": "+420123456748"},
            {"name": "Rozvoz poledního menu 3, tel:", "price": "123 456 748"},
            {"name": "Rozvoz poledního menu 4, tel:", "price": "123456748"},
        ]

        cleaned = self.cleaner.clean_daily_menu(menus)

        self.assertEquals(len(menus), len(cleaned))

        for menu in cleaned:
            self.assertIsNone(menu['price'])

    def test_line_remove(self):
        menus = [
            {"name": "Čočková..............................", "price": "45 Kč"},
            {"name": "Čočková----------------------------", "price": "45 Kč"},
            {"name": "Čočková _____________________________", "price": "45 Kč"},
        ]
        cleaned = self.cleaner.clean_daily_menu(menus)
        self.assertEqual(1, len(cleaned))

        for menu in cleaned:
            self.assertEquals(menu['name'], 'Čočková')

    def test_name_trimmer(self):
        menus = [
            {"name": "Bramboračka ", "price": "45 Kč"},
            {"name": "Bramboračka, cena 45 Kc", "price": "45 Kč"},
            {"name": "Bramboračka _____________________________ ", "price": "45 Kč"},
        ]
        cleaned = self.cleaner.clean_daily_menu(menus)
        self.assertEqual(1, len(cleaned))

        for menu in cleaned:
            self.assertEquals(menu['name'], 'Bramboračka')

    def test_duplicates(self):
        menus = [
            {"name": "TEMPURA MORIAWASE", "price": ""},
            {"name": "TEMPURA MORIAWASE", "price": ""},
            {"name": "TEMPURA MORIAWASE", "price": ""},
        ]

        cleaned = self.cleaner.clean_daily_menu(menus)
        self.assertEqual(1, len(cleaned))

    def test_splitted_menu_name(self):

        menus = [{"name": "Těstoviny linguine s mořskými plody,", "price": ''},
                 {"name": "česnekem, feferonkou, petrželkou a", "price": ''},
                 {"name": "citrónovým olivovým olejem, zdobené rukolou", "price": ''}]

        cleaned = self.cleaner.clean_daily_menu(menus)
        self.assertEqual(1, len(cleaned))
