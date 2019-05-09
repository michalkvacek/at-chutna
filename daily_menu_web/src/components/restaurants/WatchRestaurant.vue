<template>
    <div v-if="isLoggedIn">


        <v-btn flat
               color="orange"
               class="watched-restaurant-btn"
               @click.prevent="starRestaurant(restaurant)"
               v-if="$store.getters.isRestaurantWatched(restaurant)">
            Sledováno
            <v-icon>mdi-star</v-icon>
        </v-btn>

        <v-btn flat
               color="orange"
               class="not-watched-restaurant-btn"
               @click.prevent="starRestaurant(restaurant)"
               v-if="!$store.getters.isRestaurantWatched(restaurant)">
            Sledovat
            <v-icon>mdi-star-outline</v-icon>
        </v-btn>
    </div>
</template>

<script>

    import {mapGetters} from "vuex";

    export default {
        name: "watch-restaurant-btn",
        props: ['restaurant'],
        computed: {
            ...mapGetters(['isLoggedIn'])
        },
        methods: {
            starRestaurant(restaurant) {

                if (this.$store.getters.isRestaurantWatched(restaurant)) {
                    // already watched, user wants to remove it from watched
                    this.$http.delete(this.API_URL + '/restaurants/watched/' + restaurant.id + '/').then(
                        (response) => {
                            this.$store.commit('unwatchRestaurant', response.data);
                            this.isWatched = false;
                        }
                    )
                } else {
                    this.$http.post(this.API_URL + '/restaurants/watched/', {
                        restaurant_id: restaurant.id,
                        watch: !this.isWatched
                    }).then(
                        (response) => {
                            this.$store.commit('watchRestaurant', response.data);
                            this.isWatched = true;
                        }
                    )
                }
            }
        }
    }
</script>