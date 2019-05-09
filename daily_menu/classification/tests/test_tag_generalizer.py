from django.test import TestCase

from classification.elasticsearch.finders.finders import RecipesFinder
from classification.models import TagGeneralization
from classification.tagger.tag_generalizer import TagsGeneralizer


class TestTagGeneralizer(TestCase):

    def setUp(self):

        data = {
            'maso': [
                'divočina',
            ],
            'divočina': [
                'kanci'
            ],
            'těstoviny': [
                'farfalle',
            ]
        }

        finder = RecipesFinder()

        for extra_tag in data:
            for tag in data[extra_tag]:
                canonical = " ".join(finder.analyze_tokens(tag))
                extra_canonical = " ".join(finder.analyze_tokens(extra_tag))

                TagGeneralization(
                    tag=tag,
                    tag_canonical=canonical,
                    extra_tag=extra_tag,
                    extra_tag_canonical=extra_canonical).save()

        self.expander = TagsGeneralizer()

    def test_pasta(self):
        tags = {'farfalle'}
        extra_tags = self.expander.get_tags("foo", tags)

        self.assertIn('testovina', extra_tags)

    def test_nothing_removed(self):
        tags = {"foo"}

        extra_tags = self.expander.get_tags('foo', tags)

        self.assertEqual(1, len(extra_tags))

    def test_cyclic_add(self):
        tags = {'kanec'}
        extra_tags = self.expander.get_tags("foo", tags)

        self.assertIn('maso', extra_tags)
        self.assertIn('divocina', extra_tags)
