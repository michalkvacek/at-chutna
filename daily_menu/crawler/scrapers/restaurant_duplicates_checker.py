from restaurants.models import Restaurant


class RestaurantDuplicatesChecker():
    accuracy = 0.001

    def __init__(self):
        restaurants = Restaurant.objects.all()
        self.restaurants = {}
        for restaurant in restaurants:

            key = self._tokenize_name(restaurant.name)

            if restaurant.name not in self.restaurants:
                self.restaurants[key] = []

            self.restaurants[key].append((restaurant.gps_lat, restaurant.gps_lng))

    def _tokenize_name(self, name):
        return name.strip().lower()

    def _is_on_same_place(self, gps1, gps2):

        if gps2[0] is None or gps2[1] is None:
            return True

        if gps1[0] is None or gps1[1] is None:
            return True

        return gps1[0] - self.accuracy <= gps2[0] <= gps1[0] + self.accuracy and \
               gps1[1] - self.accuracy <= gps2[1] <= gps1[1] + self.accuracy

    def _check_restaurant(self, name, gps):
        positions = self.restaurants[name]

        for position in positions:
            if self._is_on_same_place(gps, position):
                return True

        return False

    def already_exists(self, name, gps):
        name = self._tokenize_name(name)

        if name in self.restaurants:
            exists = self._check_restaurant(name, gps)
            if exists:
                return True

        return False
