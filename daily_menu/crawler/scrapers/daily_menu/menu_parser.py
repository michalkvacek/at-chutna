import re


class MenuParser:
    def __init__(self):
        self.dates_words = ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', ' sobota', 'neděle']
        self.dates_regexps = ['[0-9]{1,2}\.\s?[0-9]{1,2}\.']

    def _is_date(self, heading):
        # pondeli
        if heading.lower() in self.dates_words:
            return True

        # pondeli, 21. 3
        for day in self.dates_words:
            if day in heading.lower():
                return True

        # 21. 3.
        for regexp in self.dates_regexps:
            if re.match(regexp, heading):
                return True

        return False

    def get_menu(self):
        raise NotImplementedError('Not implemented!')

    def _get_date(self, date_string):
        return date_string.split(' ')[0]
