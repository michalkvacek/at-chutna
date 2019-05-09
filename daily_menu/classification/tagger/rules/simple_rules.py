class BaseRule:
    name = ""
    must_contain_all = []
    cannot_contain = []


class Vegetarian(BaseRule):
    name = "vegetarian"
    cannot_contain = ['maso']


class Vegan(BaseRule):
    name = "vegan"
    cannot_contain = ['maso', 'vejce', 'syr', 'mleko', 'maslo', 'tvaroh']
