<template>
    <div class="mt-5 restaurants-with-menu-list">
        <!--    <v-card>-->
        <!--        <v-card-title primary-title>-->
        <!--            <div>-->
        <h2 class="display-3 text-xs-center">Dnešní menu</h2>
        <!--            </div>-->
        <!--        </v-card-title>-->

        <!--        <v-card-text>-->

        <v-alert type="error" :value="error">
            Při načítání seznamu restaurací se stala chyba. Zkuste to prosím za okamžik znovu.
        </v-alert>


        <v-alert type="info" :value="waitingForLocation">
            Povolte prosím přístup k poloze, abychom byli schopni vám zobrazit seznam restaurací ve
            vašem okolí.
        </v-alert>


        <v-alert :value="!waitingForLocation && !loading && !error && restaurants.length === 0"
                 type="warning"
                 outline>
            <span v-if="locationAllowed && locationUsed">
                Zdá se, že v okolí nejsou žádné restaurace s denním menu. Načíst <a
                    @click.prevent="loadAllRestaurants()">všechny restaurace</a>?
            </span>
            <span v-else>
                Zdá se, že žádné ze sledovaných restaurací nemají vložené denní menu.
            </span>
        </v-alert>

        <v-container grid-list-sm fluid v-if="restaurants.length > 0">
            <v-layout row wrap justify-center>
                <restaurant-detail-list :restaurant="restaurant"
                                        class="mt-2 restaurant-detail-item"
                                        v-for="restaurant in restaurants"
                                        :key="restaurant.id">

                </restaurant-detail-list>
            </v-layout>
        </v-container>
        <!--        </v-card-text>-->
        <v-layout justify-center>

            <v-flex class="grow">

                <v-alert type="info" class="loading" :value="loading" outline>
                    Probíhá načítání restaurací.
                </v-alert>

                <v-btn class="load-more" @click="loadFeaturedRestaurants" v-if="!error && !allLoaded && remaining > 0">
                    Načíst další stránku (zbývá {{remaining}})
                </v-btn>

                <v-alert type="info" :value="allLoaded && restaurants.length > 0" class="text-xs-center">
                    A víc toho není...
                </v-alert>
            </v-flex>
        </v-layout>
        <!--    </v-card>-->
    </div>
</template>

<script>
    import RestaurantDetailList from "./detail/ListView";

    export default {
        name: "restaurants-with-menu",
        data() {
            return {
                restaurants: [],
                loading: false,
                error: false,
                waitingForLocation: true,
                locationAllowed: false,
                locationUsed: false,
                url: this.API_URL + '/today_menu/restaurants/',
                allLoaded: false,
                totalCount: 0
            }
        },
        computed: {
            remaining() {
                return this.totalCount - this.restaurants.length;
            }
        },
        components: {
            RestaurantDetailList,
        },
        methods: {
            loadAllRestaurants() {
                this.url = this.API_URL + '/today_menu/restaurants/'

                this.locationUsed = false;

                this.loadFeaturedRestaurants()
            },
            loadFeaturedRestaurants() {
                if (this.url == null) {
                    this.allLoaded = true;
                    return;
                }

                this.waitingForLocation = false;
                this.loading = true;

                this.$http.get(this.url).then(
                    response => {
                        let results = response.data.results;
                        for (let i in results) {
                            this.restaurants.push(results[i]);
                        }

                        this.url = response.data.next;
                        this.allLoaded = this.url == null;
                        this.totalCount = response.data.count;

                        this.loading = false;
                        this.error = false;
                    }).catch(
                    () => {
                        this.error = true;
                        this.loading = false;
                    })
            }
        },

        mounted() {
            this.$getLocation().then(coordinates => {
                // load nearby restaurants


                if (typeof coordinates.lat !== 'undefined' && typeof coordinates.lng !== 'undefined') {
                    this.locationAllowed = true;
                    this.locationUsed = true;
                    this.url += "?lat=" + coordinates.lat + "&lng=" + coordinates.lng;
                } else {
                    this.locationAllowed = false;

                }

                this.loadFeaturedRestaurants();

            }).catch(() => {
                // load some predefined restaurants
                this.locationAllowed = false;

                this.loadFeaturedRestaurants();
            })
        }
    }
</script>
