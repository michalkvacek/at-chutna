<template>
    <div>
        <vue-title v-if="restaurant" :title="'Restaurace: '+restaurant.name"></vue-title>

        <v-alert type="info" :value="loading">Načítám detail restaurace</v-alert>

        <v-layout justify-center v-if="!loading">
            <v-flex md11>
                <v-card>

                    <map-with-markers v-if="markers.length > 0" :center="markers[0]"
                                      :markers="markers"></map-with-markers>


                    <v-card-title primary-title class="text-xs-center">
                        <div class="grow">
                            <h1 class="headline mb-0">
                                {{restaurant.name}}
                            </h1>

                            <watch-restaurant-btn :restaurant="restaurant"></watch-restaurant-btn>


                            <restaurant-address :address="restaurant.address"></restaurant-address>

                        </div>


                    </v-card-title>
                    <v-card-text>
                        <v-layout justify-center>
                            <v-flex md6>
                                <daily-menu-list :max=null :list="restaurant.daily_menu"></daily-menu-list>

                                <p v-if="restaurant.menu_url">
                                    <a :href="restaurant.menu_url" target="_blank">Zdroj:
                                        {{getDomainName(restaurant.menu_url)}}</a>
                                </p>
                            </v-flex>
                        </v-layout>


                    </v-card-text>


                </v-card>
            </v-flex>
        </v-layout>
    </div>
</template>

<script>
    import DailyMenuList from "../daily_menu/DailyMenuList";
    import RestaurantAddress from "./address/Address";
    import MapWithMarkers from "../map/MapWithMarkers";
    import WatchRestaurantBtn from "./WatchRestaurant";

    export default {
        name: "restaurant-info",
        props: ['id'],
        components: {
            WatchRestaurantBtn,
            MapWithMarkers,
            RestaurantAddress,
            DailyMenuList,
        },

        data() {
            return {
                restaurant: null,
                loading: true,
                error: false,
                markers: []
            }
        },
        methods: {
            getDomainName(url) {
                return url.replace('http://', '').replace('https://', '').split(/[/?#]/)[0];
            },
        },

        mounted() {
            this.$http.get(this.API_URL + '/restaurants/' + this.id + '/').then(
                response => {
                    this.restaurant = response.data;

                    if (this.restaurant.gps_lat != null && this.restaurant.gps_lng != null) {
                        this.markers.push({"lat": this.restaurant.gps_lat, "lng": this.restaurant.gps_lng});
                    }

                    this.loading = false;
                    this.error = false;
                }).catch(
                () => {
                    this.error = true;
                    this.loading = false;

                })
        }
    }
</script>