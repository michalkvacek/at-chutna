
from classification.tagger.recipe_tagger import RecipeTagger, TagExpander
from classification.tagger.tag_generalizer import TagsGeneralizer
from classification.tagger.tags_deducer import TagsDeducer


class DailyMenuTagger:
    def __init__(self):
        self.recipe_tagger = RecipeTagger()

        self.taggers = [
            self.recipe_tagger,
            TagExpander(),
            TagsGeneralizer(),
            TagsDeducer()
        ]

    def get_tags(self, menu_name, tags=None):
        # static tagging
        all_tags = self.recipe_tagger.get_static_tags(menu_name, include_separate_words=False)

        for tagger in self.taggers:
            extra_tags = tagger.get_tags(menu_name, all_tags)
            all_tags.update(extra_tags)

        return set(all_tags)
