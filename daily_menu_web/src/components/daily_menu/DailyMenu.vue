<template>
    <div class="menu">
        <strong v-if="restaurant">
            <router-link
                    :to="{name: 'restaurant_detail', params: {id: restaurant.id}}">{{restaurant.name}}</router-link>:
        </strong>

        {{menu.name}}<span v-if="menu.price > 0">, {{menu.price}} Kč</span>
        <daily-menu-rating v-if="isLoggedIn" :menu="menu"></daily-menu-rating>

        <slot></slot>
    </div>
</template>

<style scoped>
    .menu {
        margin: 10px 0;
        font-size: 120%;
    }
</style>

<script>
    import DailyMenuRating from "./Rating";
    import {mapGetters} from "vuex";

    export default {
        name: "daily-menu",
        components: {DailyMenuRating},
        props: ['menu', 'restaurant'],
        computed: {
            ...mapGetters(['isLoggedIn'])
        }
    }
</script>