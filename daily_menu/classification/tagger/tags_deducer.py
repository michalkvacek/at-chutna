from classification.tagger.rules.simple_rules import Vegetarian, Vegan


class TagsDeducer:
    def __init__(self):
        self.rules = [
            Vegetarian,
            Vegan,
        ]

    def get_tags(self, menu_name, tags=[]):
        tags_string = ";".join(tags)

        new_tags = set()

        for rule in self.rules:
            contains_forbidden = False
            contains_all_required = True

            for forbidden_string in rule.cannot_contain:
                if forbidden_string in tags_string:
                    contains_forbidden = True
                    break

            for required_string in rule.must_contain_all:
                if required_string not in tags_string:
                    contains_all_required = False

                    break

            if not contains_forbidden and contains_all_required:
                new_tags.add(rule.name)

        return new_tags
