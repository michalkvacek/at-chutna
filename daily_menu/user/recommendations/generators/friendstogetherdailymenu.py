from user.recommendations.generators.mostsimilardailymenu import MostSimilarDailyMenu


class FriendsTogetherDailyMenu:
    most_similar = MostSimilarDailyMenu()

    def get_recommendations_for_friends(self, max, friendships, my_location):
        friends_location = my_location if my_location.recommendation_type == 'position' else None
        recommendations_for_friends = {}

        # create recommendations for friends
        for friendship in friendships:
            if not friendship.lunch_together:
                # user does not want to have lunch with this user
                continue

            recommendations_for_friends[friendship.friend] = self.most_similar.get_recommendation_for_user(
                friendship.friend,
                max,
                'personal',
                friends_location
            )['user_recommendations']

        return recommendations_for_friends

    def get_recommendation_for_user(self, user, max=5, type='friends', recommendation_type='restaurants'):
        friendships = user.friends_set.all()

        if len(friendships) == 0:
            return {
                'user_recommendations': [],
                'friends_recommendations': []
            }

        my_location = self.most_similar.get_location(user, type='friends', location=None)
        my_recommendations = self.most_similar.get_recommendation_for_user(
            user,
            max,
            'personal',
            my_location)['user_recommendations']

        recommendations_for_friends = self.get_recommendations_for_friends(max, friendships, my_location)

        if len(recommendations_for_friends) == 0:
            return {
                'user_recommendations': [],
                'friends_recommendations': []
            }

        # ziskani doporuceni od pratel
        my_restaurants = set([menu[0].restaurant.id for menu in my_recommendations])
        common_restaurants = {}
        friends_recommendations = {}
        for friend in recommendations_for_friends:
            friends_restaurants = set([menu[0].restaurant.id for menu in recommendations_for_friends[friend]])
            common_restaurants[friend] = friends_restaurants & my_restaurants

        # nalezeni doporuceni pro pratele ve spolecnych restauracich
        for friend in recommendations_for_friends:
            for recommendation in recommendations_for_friends[friend]:
                restaurant = recommendation[0].restaurant
                if restaurant.id in common_restaurants[friend]:

                    if restaurant.id not in friends_recommendations:
                        friends_recommendations[restaurant.id] = {}

                    if friend not in friends_recommendations[restaurant.id]:
                        friends_recommendations[restaurant.id][friend] = set()

                    friends_recommendations[restaurant.id][friend].add(recommendation[0])

        # merge friends and user's recommendations
        final_recommendation = []
        for my_recommendation in my_recommendations:
            restaurant_id = my_recommendation[0].restaurant.id

            if restaurant_id not in friends_recommendations or len(friends_recommendations[restaurant_id]) == 0:
                continue

            friends = [k for k in friends_recommendations[restaurant_id]]
            final_recommendation.append((my_recommendation[0], friends))

        final_friends_recommendations = []
        for restaurant_id in friends_recommendations:
            final_friends_recommendations.append(friends_recommendations[restaurant_id])

        return {
            'user_recommendations': final_recommendation,
            'friends_recommendations': final_friends_recommendations
        }
