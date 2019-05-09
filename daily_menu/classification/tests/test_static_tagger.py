from django.test import TestCase
from classification.tagger.recipe_tagger import RecipeTagger
from classification.tagger.static_tagger import StaticTagger


class TestStaticTagger(TestCase):

    def setUp(self):
        self.tagger = StaticTagger()

    def test_static_tags_count(self):
        name = "150g Svíčková na smetaně s houskovým knedlíkem, brusinkami a domácí limonádou"

        tags = self.tagger.get_tags(name)
        self.assertEqual(5, len(tags))

    def test_static_tags(self):
        expected = ['brusinkami', 'svíčková', 'smetaně', 'houskovým knedlíkem', 'domácí limonádou']
        for tag in expected:
            self.assertIn(tag, expected)
