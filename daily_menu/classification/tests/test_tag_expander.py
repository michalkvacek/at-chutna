from django.test import TestCase
from classification.tagger.recipe_tagger import RecipeTagger, TagExpander


class TestTagExpander(TestCase):

    def setUp(self):
        self.expander = TagExpander()

    def test_expand(self):
        tags = ['hovezi klizka']
        extra_tags = self.expander.get_tags("foo", tags)

        self.assertNotEqual(0, len(extra_tags))

