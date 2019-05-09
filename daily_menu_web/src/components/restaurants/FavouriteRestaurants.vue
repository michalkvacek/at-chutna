<template>
<!--    <v-container grid-list-sm>-->
<!--        <v-layout row wrap>-->

            <div>
                <v-alert :value="error" type="error">
                    Nelze načíst oblíbené restaurace. Zkuste to znovu za malý okamžik.
                </v-alert>

                <v-alert :value="loading" type="info" outline>
                    Probíhá načítání seznamu oblíbených restaurací.
                </v-alert>


                <v-alert :value="!loading && !error && restaurants.length === 0" type="warning" outline>
                    Aktuálně nemáte žádné oblíbené restaurace. Označujte jednotlivá jídla, abychom byli schopni vám
                    zobrazit
                    tento seznam.
                </v-alert>


                <div v-if="!error && !loading && restaurants.length > 0">
                    <h2>Oblíbené restaurace</h2>
                    <div>Do těchto restaurací často chodíte a nebo vás láká jejich denní nabídka.</div>

                    <v-layout row wrap>
                        <restaurant-detail-list
                                v-for="restaurant in restaurants"
                                :key="restaurant.id"
                                :restaurant="restaurant">
                        </restaurant-detail-list>
                    </v-layout>


                    <favourite-restaurants-help v-if="restaurants.length > 0"></favourite-restaurants-help>
                </div>
            </div>

<!--        </v-layout>-->
<!--    </v-container>-->
</template>
<script>

    import RestaurantDetailList from "./detail/ListView";
    import FavouriteRestaurantsHelp from "./FavouriteRestaurantsHelp";

    export default {
        name: "favourite-restaurants",
        components: {FavouriteRestaurantsHelp, RestaurantDetailList},
        data() {
            return {
                restaurants: [],
                loading: true,
                error: false
            }
        },
        mounted() {
            this.$http.get(this.API_URL + '/restaurants/favourite/').then(
                response => {
                    this.restaurants = response.data.results;

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
