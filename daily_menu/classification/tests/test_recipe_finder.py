from django.test import TestCase

from classification.elasticsearch.finders.finders import RecipesFinder


class TestRecipeFinder(TestCase):

    def setUp(self):
        self.finder = RecipesFinder()

    def test_analyze_tokens(self):

        data = self.finder.analyze_tokens('hovězím masem')

        self.assertEqual(2, len(data))
        self.assertIn('hovezi', data)
        self.assertIn('maso', data)

    def test_find(self):
        name = "Bramboracka"
        recipes = self.finder.find(name)

        for recipe in recipes:
            self.assertIn('name', recipe)
            self.assertIn('ingredients', recipe)
            self.assertIn('tags', recipe)
            self.assertIn('categories', recipe)

    def test_not_empty_info(self):
        name = "Bramboracka"
        recipes = self.finder.find(name)

        for recipe in recipes:
            extra = recipe['ingredients'] + recipe['tags'] + recipe['categories']

            self.assertNotEqual(0, len(extra))
