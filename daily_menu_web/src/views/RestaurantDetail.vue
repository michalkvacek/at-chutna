<template>
    <restaurant-info :id="this.$route.params.id"></restaurant-info>
</template>

<script>

    import RestaurantInfo from "../components/restaurants/RestaurantInfo";

    export default {
        name: 'restaurant-detail',
        components: {
            RestaurantInfo
        },

    }
</script>