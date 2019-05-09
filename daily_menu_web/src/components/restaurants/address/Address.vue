<template>
    <div v-if="address" class="address">Adresa: {{address}}</div>
</template>

<script>

    import AddressMap from "../../map/MapWithMarkers";

    export default {
        name: "restaurant-address",
        components: {AddressMap},
        props: ['address']
    }
</script>