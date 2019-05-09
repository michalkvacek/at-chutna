from classification.models import TagGeneralization


class TagsGeneralizer():
    extra_tags = {}

    def _loaded(self):
        """
        Checks if extra tags were loaded previously
        :return:
        """
        return len(self.extra_tags) > 0

    def _load_extra_tags(self):
        """
        Load extra tags
        :return:
        """

        if self._loaded():
            return

        extra_tags = TagGeneralization.objects.all()
        for tag in extra_tags:
            if tag.extra_tag_canonical not in self.extra_tags:
                self.extra_tags[tag.extra_tag_canonical] = []

            self.extra_tags[tag.extra_tag_canonical].append(tag.tag_canonical)

    def get_tags(self, menu_name, tags=None):
        """
        Get generalized tags for given menu with tags
        :param menu_name:
        :param tags:
        :return:
        """
        if tags is None:
            tags = set()

        self._load_extra_tags()
        all_tags = " ".join(tags)

        original_size = len(tags)
        tag_added = True
        while tag_added:
            tag_added = False

            for extra in self.extra_tags:
                for t in self.extra_tags[extra]:
                    if t in all_tags:
                        tags.add(extra)

                        if len(tags) > original_size:
                            all_tags += " " + extra
                            tag_added = True

                        original_size = len(tags)

        return tags
