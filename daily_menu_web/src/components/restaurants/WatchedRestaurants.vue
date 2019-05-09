<template>
    <!--    <v-container grid-list-md text-xs-center v-if="watched_restaurants.length > 0">-->

    <div v-if="watched_restaurants.length > 0">
        <h2 class="watched-restaurants-heading">Sledované restaurace</h2>
        <v-layout wrap class="watched-restaurants-list">
            <restaurant-detail-list v-for="restaurant in watched_restaurants"
                                    :key="restaurant.id"
                                    :restaurant="restaurant">
            </restaurant-detail-list>
        </v-layout>

    </div>


    <!--    </v-container>-->
</template>


<script>

    import RestaurantDetailList from "./detail/ListView";
    import {mapState} from "vuex";

    export default {
        name: "watched-restaurants",
        components: {RestaurantDetailList},
        data() {
            return {
                restaurants: [],
                loading: true,
                error: false
            }
        },
        computed: {
            ...mapState(['watched_restaurants'])
        }
    }
</script>
