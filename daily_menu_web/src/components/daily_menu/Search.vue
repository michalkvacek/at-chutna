<template>

    <v-flex>
        <v-alert type="info" :value="loading">Probíhá vyhledávání</v-alert>

        <v-form @submit.prevent="search" id="search-form">
            <v-text-field v-model="term"
                          required
                          @input="submitted = false"
                          label="Vyhledávání dnešního menu nebo restaurací">
            </v-text-field>

            <v-btn primary type="submit" form="search-form">Vyhledat</v-btn>
        </v-form>

        <v-container grid-list-sm fluid v-if="submitted && data.length > 0">
            <v-layout row wrap justify-center>
                <v-card flat class="grow">
                    <v-card-title primary-title>
                        <h2>Výsledky vyhledávání pro "{{term}}"</h2>
                    </v-card-title>
                    <v-card-text>
                        <v-layout row wrap>
                            <restaurant-detail-list :restaurant="restaurant"
                                                    class="mt-2"
                                                    v-for="restaurant in data"
                                                    :key="restaurant.id">

                            </restaurant-detail-list>
                        </v-layout>
                    </v-card-text>
                </v-card>
            </v-layout>
        </v-container>

        <v-alert type="info" :value="term !== '' && submitted && data.length === 0">
            Termín "{{term}}" se nenachází v žádném dnešním menu ani v názvu restaurace.
        </v-alert>

    </v-flex>


</template>

<script>
    import DailyMenuList from "./DailyMenuList";
    import RestaurantDetailList from "../restaurants/detail/ListView";

    export default {
        name: "search",
        components: {RestaurantDetailList, DailyMenuList},
        data() {
            return {
                term: '',
                submitted: false,
                data: [],
                loading: false
            }

        },

        methods: {
            search() {

                if (this.term.length === 0) {
                    return;
                }

                this.loading = true;

                this.$http.get(this.API_URL + '/search/?q=' + this.term).then((response) => {
                    this.data = response.data;
                    this.loading = false
                    this.submitted = true;
                })
            }
        }
    }
</script>