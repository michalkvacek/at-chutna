<template>


    <div>
        <v-layout row wrap justify-center v-if="isLoggedIn">
            <vue-title title="Dnešní nabídka restaurací"></vue-title>

            <div class="grow">
                <h2 class="display-3 my-3 text-xs-center">Dnes doporučujeme</h2>

                <recommended-daily-menus type="all"></recommended-daily-menus>
            </div>
        </v-layout>


        <restaurants-with-menu></restaurants-with-menu>
    </div>
</template>

<script>
    import RestaurantsWithMenu from "../components/restaurants/RestaurantsWithMenu";
    import RecommendedDailyMenus from "../components/daily_menu/RecommendationList";
    import {mapGetters} from "vuex";
    export default {
        name: 'home',
        computed: {
            ...mapGetters(['isLoggedIn'])
        },
        components: {
            RecommendedDailyMenus,
            RestaurantsWithMenu,
        }
    }
</script>
