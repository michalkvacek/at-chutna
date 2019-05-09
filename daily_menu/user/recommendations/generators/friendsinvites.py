

class FriendsInvites:
    def get_recommendation_for_user(self, user, max=5, type='friends', recommendation_type='restaurants'):
        return {
            'user_recommendations': [],
            'friends_recommendations': []
        }