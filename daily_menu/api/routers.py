from rest_framework import routers

from api.viewsets import *

router = routers.DefaultRouter()

router.register(r'today_menu/restaurants', RestaurantsWithTodayMenuViewSet)
router.register(r'today_menu/recommended', RecommendedDailyMenusViewSet)
router.register(r'daily_menu/rating', DailyMenuRatingViewSet)
router.register(r'daily_menu/not_meal', DailyMenuRatingViewSet)

router.register(r'daily_menu/cousine', CousineTaggerViewSet)

router.register(r'restaurants/favourite', FavouriteRestaurantViewSet)
router.register(r'restaurants/watched', WatchedRestaurantsViewSet)
router.register(r'restaurants', RestaurantViewSet)

router.register(r'me/preferences', PreferencesViewSet)
router.register(r'me/friends', FriendsViewSet)
router.register(r'me/location', RecommendationLocationViewSet)
router.register(r'me', MeViewSet)
router.register(r'search', SearchView)
