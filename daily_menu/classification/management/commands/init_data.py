from django.core.management import BaseCommand
from django.utils import timezone

from classification.elasticsearch.finders.finders import IngredientsFinder
from classification.models import TagGeneralization
from crawler.models import RecipeIngredientCrawler
from restaurants.models import Cousine
from user.models import Recommender


def init_tag_generalizations():
    ingredients_finder = IngredientsFinder()

    data = {
        'maso': [
            'krkovice',
            'krkovička',
            'slanina',
            'líčka',
            'hovězí',
            'vepř',
            'kuře',
            'kachní',
            'kachna',
            'řízek',
            'steak',
            'ryba',
            'divočina',
            'drůbež',
            'párek',
            'choriz',
        ],
        'divočina': [
            'kančí',
            'srnční',
            'jelení',
        ],
        'ryba': [
            'candat',
            'kapr',
            'sumec',
            'losos',
            'tunak',
            'makrela',
            'pangasius'
        ],
        'syr': [
            'chedar',
            'cheddar',
            'emental',
            'hermelin',
            'brie',
            'gouda',
            'camembert',
            'roquefort',
            'raclette',
            'parmezan',
            'halloumi'
        ],
        'rajce': [
            'rajcat',
            'protlak',
            'rajsk',
        ],
        'paprika': [
            'paprik'
        ],

        'těstoviny': [
            'spageta',
            'farfalle',
            'tortellini',
            'ravioli',
            'cappelleti',
            'canelloni',
            'spaghetti',
            'spaghettini',
            'bucatini',
            'maccheroni',
            'linguine',
            'fettuccine',
            'tagliatelle',
            'pappardelle',
            'penne',
            'pizzoccheri',
            'rigatoni',
            'lasagne',
            'farfalle',
            'fusilli',
            'gnocchi',
            'radiatori',
            'cannelloni',
            'orecchiette',
            'cavatelli',
            'casarecce',
            'rotelle',
            'spätzle',
            'stelline',
            'peperini',
            'alfabetti',
            'anellini',
            'capellini tagliati',
            'conchigliette',
            'farfalline',
        ],
        'omacka': [
            'boloňská',
            'znojemská',
            'koprova',
            'rajska',
            'svíčková'
        ],
        'brambory': [
            'grenaille',
            'hranolky',
            'brambor',
            'ameriky'
        ],
        'drůbež': [
            'kuře',
            'kachna',
            'kachní'
        ],
        'mořské': [
            'krab', 'chobnotnice', 'slávky', 'krevety', 'krevetový', 'sépie', 'sépiový'
        ],
        'houby': [
            'hřib',
            'žampiony',
            'žampionový',
            'hlíva'
        ]

    }

    TagGeneralization.objects.all().delete()
    for extra_tag in data:
        for tag in data[extra_tag]:
            canonical = " ".join(ingredients_finder.analyze_tokens(tag))
            extra_canonical = " ".join(ingredients_finder.analyze_tokens(extra_tag))

            TagGeneralization(
                tag=tag,
                tag_canonical=canonical,
                extra_tag=extra_tag,
                extra_tag_canonical=extra_canonical).save()


def init_cousines():
    cousines = [
        {'name': 'Indická kuchyně', 'classification_column': 'indian'},
        {'name': 'Vietnamská kuchyně', 'classification_column': 'vietnamese'},
        {'name': 'Mexická kuchyně', 'classification_column': 'mexican'},
        {'name': 'Česká kuchyně', 'classification_column': 'czech'},
        {'name': 'Americká kuchyně', 'classification_column': 'american'},
        {'name': 'Čínská kuchyně', 'classification_column': 'chinese'},
        {'name': 'Japonská kuchyně', 'classification_column': 'japanese'},
        {'name': 'Italská kuchyně', 'classification_column': 'italian'},
        {'name': 'Polévky', 'classification_column': 'soup'},
        {'name': 'Sladká jídla', 'classification_column': 'sweet'}
    ]

    Cousine.objects.all().delete()

    for cousine in cousines:
        Cousine(name=cousine['name'], classification_column=cousine['classification_column']).save()


def init_recipe_crawlers():
    crawlers = [
        {"name": 'Recepty.cz', 'downloader': 'recipes.ReceptyDownloader'},
        {"name": 'TopRecepty.cz', 'downloader': 'recipes.TopReceptyDownloader'},
    ]

    RecipeIngredientCrawler.objects.all().delete()

    for crawler in crawlers:
        RecipeIngredientCrawler(name=crawler['name'], crawler_class=crawler['downloader'], next_visit_interval=90,
                                next_visit=timezone.now().date()).save()


def init_recommenders():
    recommenders = [
        {"name": 'Dle tvých chutí', "class": 'MostSimilarDailyMenu', 'order': 1, 'description': '',
         'with_friends': False},
        {"name": 'Oběd s přáteli', "class": 'FriendsTogetherDailyMenu', 'order': 2,
         'description': 'V těchto restauracích si vybereš ty i tví přátelé', 'with_friends': True},
        {"name": 'Pozvání od přátel', "class": 'FriendsInvites', 'order': 3,
         'description': 'Tito přátelé by s vámi chtěli jít na oběd.', 'with_friends': True},
    ]

    Recommender.objects.all().delete()

    for recommender in recommenders:
        Recommender(
            name=recommender['name'],
            recommendation_class=recommender['class'],
            order=recommender['order'],
            description=recommender['description'],
            with_friends=recommender['with_friends']
        ).save()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        init_tag_generalizations()
        init_cousines()
        init_recipe_crawlers()
        init_recommenders()
