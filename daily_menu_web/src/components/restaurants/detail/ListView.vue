<template>
    <v-flex xs12 sm6 md4 grow>
        <v-card height="100%" class="restaurant mx-3 my-5">

            <v-card-title primary-title>
                <div class="grow text-xs-center">
                    <h3 class="headline mb-0">
                        <router-link :to="{name: 'restaurant_detail', params: {id: restaurant.id}}" class="restaurant-detail-link">
                            {{restaurant.name}}
                        </router-link>
                    </h3>
                    <div>
                        <restaurant-address :address="restaurant.address"></restaurant-address>
                    </div>
                </div>
            </v-card-title>

            <v-card-text>
                <daily-menu-list :list="restaurant.daily_menu"></daily-menu-list>

                <p v-if="restaurant.menu_url">
                    <a :href="restaurant.menu_url" target="_blank">Zdroj: {{getDomainName(restaurant.menu_url)}}</a>
                </p>
            </v-card-text>

            <v-card-actions>
                <v-btn flat :to="{name: 'restaurant_detail', params: {id: restaurant.id}}">
                    <v-icon>mdi-information-outline</v-icon>
                </v-btn>

                <v-spacer></v-spacer>


                <watch-restaurant-btn :restaurant="restaurant"></watch-restaurant-btn>
            </v-card-actions>
        </v-card>
    </v-flex>
</template>

<script>
    import DailyMenuList from "../../daily_menu/DailyMenuList";
    import RestaurantAddress from "../address/Address";
    import {mapGetters} from "vuex";
    import WatchRestaurantBtn from "../WatchRestaurant";

    export default {
        name: "restaurant-detail-list",
        props: ['restaurant'],
        components: {
            WatchRestaurantBtn,
            RestaurantAddress,
            DailyMenuList
        },
        computed: {
            ...mapGetters(['isLoggedIn'])
        },

        methods: {
            getDomainName(url) {
                return url.replace('http://', '').replace('https://', '').split(/[/?#]/)[0];
            },


        }
    }
</script>