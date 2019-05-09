<template>


    <v-container fluid pb-0>
        <v-layout>

            <v-card class="grow">
                <v-card-title primary-title>
                    <div>
                        <h2>Vybrat polohu pro doporučování</h2>
                        <slot></slot>
                    </div>
                </v-card-title>
                <v-card-text>
                    <v-flex xs12 v-show="!useVisitedRestaurants">
                        <gmap-map :center="marker" v-if="marker" :zoom="zoom" ref="map"
                                  style="width:100%;  height: 400px;">
                            <gmap-marker
                                    :position="marker"
                                    @dragend="updateCoordinates"
                                    :draggable="true"></gmap-marker>
                        </gmap-map>

                    </v-flex>

                    <v-flex grow>
                        <v-alert :value="!useVisitedRestaurants && !locationEnabled" type="warning">
                            Pro nastavení aktuální polohy povol získávání polohy v prohlížeči.
                        </v-alert>

                        <v-alert type="info" :value="!useVisitedRestaurants" outline>
                            Pro doporučování budou použity restaurace v okruhu cca 5km okolo zvoleného bodu.
                        </v-alert>

                        <v-btn v-if="!useVisitedRestaurants && !currentPosition" color="green" dark
                               @click="setLocation">
                            Vybrat polohu na mapě
                        </v-btn>
                        <v-btn v-else @click="setLocation">Vybrat polohu na mapě</v-btn>

                        <v-btn v-if="!useVisitedRestaurants && currentPosition" color="green" dark
                               @click="setCurrentPosition">Aktuální pozice
                        </v-btn>
                        <v-btn v-else @click="setCurrentPosition">Aktuální pozice</v-btn>

                        <v-btn v-if="useVisitedRestaurants" color="green" dark @click="setPositionFromRestaurants">
                            Podle navštěvovaných restaurací
                        </v-btn>
                        <v-btn v-else @click="setPositionFromRestaurants">Podle navštěvovaných restaurací
                        </v-btn>
                    </v-flex>
                </v-card-text>
            </v-card>

        </v-layout>
    </v-container>
</template>


<script>
    export default {
        name: "map-with-location-input",
        props: ['type'],
        data() {
            return {
                zoom: 14,
                useVisitedRestaurants: true,
                locationEnabled: false,
                currentPosition: false,
                marker: {lat: 50.082611, lng: 14.44986}
            };
        },
        mounted() {
            this.initRecommendationPosition();
        },

        methods: {
            initRecommendationPosition() {
                this.useVisitedRestaurants = true;

                this.$http.get(this.API_URL + "/me/location/?type=" + this.type).then((response) => {
                    let location = response.data;

                    if (typeof location['type'] !== 'undefined') {
                        if (response.data.gps_lat && response.data.gps_lng) {
                            this.marker = {
                                lat: response.data.gps_lat,
                                lng: response.data.gps_lng,
                            };
                        }
                        this.useVisitedRestaurants = response.data.recommendation_type === 'restaurants';
                    }
                });
            },

            setLocation() {
                this.useVisitedRestaurants = false;
                this.currentPosition = false;
            },
            setCurrentPosition() {
                this.geolocate();

                this.useVisitedRestaurants = false;
                this.currentPosition = true;
            },
            setPositionFromRestaurants() {
                this.useVisitedRestaurants = true;
                this.handleLocationChanged(null, null)

            },
            updateCoordinates(coordinates) {
                this.marker = {
                    lat: coordinates.latLng.lat(),
                    lng: coordinates.latLng.lng()
                };
                this.currentPosition = false;


                this.handleLocationChanged(this.marker.lat, this.marker.lng)
            },
            geolocate() {
                this.$getLocation().then(coordinates => {
                    this.locationEnabled = true;

                    this.marker = coordinates;
                    this.currentPosition = true;
                    this.useVisitedRestaurants = false;

                    this.handleLocationChanged(this.marker.lat, this.marker.lng)
                }).catch(() => {
                    // load some predefined restaurants
                    this.locationEnabled = false;
                    this.currentPosition = false;
                })
            },
            handleLocationChanged(lat, lng) {

                let recommendationType = 'restaurants';
                if (lat && lng) {
                    recommendationType = 'position';
                }

                this.$http.put(this.API_URL + "/me/location/", {
                    type: this.type,
                    recommendation_type: recommendationType,
                    gps_lat: lat,
                    gps_lng: lng
                })
            }
        },


    };
</script>