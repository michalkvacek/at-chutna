import re


class StaticTagger:

    def __init__(self):
        self.prepositions = [
            's', 'se', 'na', 'k', 'a', 'z', 'bez'
        ]

    def get_tags(self, recipe_name):
        recipe_name = re.sub('[:\.,\(\)\-]+', ', ', recipe_name.lower())
        words = recipe_name.split(' ')

        tags = set()
        tag = ''

        for word in words:
            word = re.sub(r'\d+', ' ', word).strip(" ")

            if word not in self.prepositions and len(word) > 2:
                split = word.strip().endswith(',')

                tag += " " + word.strip(',')
            else:
                split = True

            if split:
                if tag.strip() != '':
                    tags.add(tag.strip())
                split = False
                tag = ''

        if tag.strip() != '':
            tags.add(tag.strip())

        return tags
