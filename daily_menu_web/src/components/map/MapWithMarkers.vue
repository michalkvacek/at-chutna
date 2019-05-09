<template>
    <div class="map">

        <gmap-map
                :center="center"
                :zoom="17"
                style="width:100%;  height: 400px;"
        >
            <gmap-marker
                    :key="index"
                    v-for="(position, index) in markers"
                    :position="position"
                    @click="center=position"
            ></gmap-marker>
        </gmap-map>
    </div>
</template>

<script>

    export default {
        name: "map-with-markers",
        props: ['markers', 'center'],
    }
</script>