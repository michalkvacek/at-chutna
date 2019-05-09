<template>
    <v-layout row wrap>
        <vue-title :title="user.first_name+' '+user.last_name+': profil'"></vue-title>

        <v-flex xs12>
            <watched-restaurants></watched-restaurants>
            <favourite-restaurants></favourite-restaurants>
        </v-flex>
    </v-layout>
</template>

<script>
    import RecommendedDailyMenus from "../../components/daily_menu/RecommendationList";
    import FavouriteRestaurants from "../../components/restaurants/FavouriteRestaurants";
    import {mapState} from "vuex";
    import WatchedRestaurants from "../../components/restaurants/WatchedRestaurants";
    import DailyMenuMarkCousine from "../../components/daily_menu/MarkCousine";

    export default {
        components: {
            DailyMenuMarkCousine, WatchedRestaurants, FavouriteRestaurants, RecommendedDailyMenus
        },

        computed: {
            ...mapState(['user'])
        },
    }
</script>