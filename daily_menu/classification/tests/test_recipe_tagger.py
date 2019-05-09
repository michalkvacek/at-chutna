from django.test import TestCase
from classification.tagger.recipe_tagger import RecipeTagger


class TestRecipeTagger(TestCase):

    def setUp(self):
        self.finder = RecipeTagger()

    def test_static_tags(self):
        static_tags = self.finder.get_static_tags('Svíčková na smetaně s houskovým knedlíkem', include_separate_words=False)

        self.assertIn('houskovy knedlik', static_tags)
        self.assertIn('svickovy', static_tags)
        self.assertIn('smetana', static_tags)

    def test_static_tags_weird(self):
        name = "s na, a k"

        tags = self.finder.get_static_tags(name)
        self.assertEqual(0, len(tags))

    def test_static_tags_empty(self):
        name = ""

        tags = self.finder.get_static_tags(name)
        self.assertEqual(0, len(tags))

