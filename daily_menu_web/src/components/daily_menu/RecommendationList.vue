<template>
    <v-layout row wrap justify-center>
        <v-alert type="info" outline :value="loading">Probíhá načítání doporučení.</v-alert>

        <v-alert type="warning" outline :value="!loading && recommendations.length === 0">
            Není k dispozici žádné doporučené menu.
        </v-alert>

        <v-flex md4 sm6 xs12 wrap grow v-for="type in recommendations" :key="type.id">
            <v-card height="100%" class="grow my-2 mx-2">
                <v-card-title primary-title>

                    <div>
                        <h3>{{type.name}}</h3>


                        {{type.description}}
                    </div>
                </v-card-title>
                <v-card-text class="grow">
                    <daily-menu
                            v-for="recommendation in type.recommendations"
                            :key="recommendation.id"
                            :menu="recommendation.daily_menu"
                            :restaurant="recommendation.restaurant">

                        <span v-for="friend in recommendation.friends" :key="friend.id">
                            <v-avatar
                                    size="20"
                                    color="grey lighten-4">
                            <img :src="friend.avatar" :title="friend.email"
                                 :alt="`friend.first_name+' '+friend.last_name`">
                        </v-avatar>
                        </span>


                    </daily-menu>
                </v-card-text>
            </v-card>
        </v-flex>
        <v-flex xs12 text-xs-center class="mt-4" v-if="type === 'friends' ">
            <v-btn @click="refreshRecommendations">Obnovit tipy</v-btn>
        </v-flex>


    </v-layout>
</template>
<script>
    import DailyMenu from "./DailyMenu";

    export default {
        name: "recommended-daily-menus",
        components: {DailyMenu},
        props: ['type'],
        data() {
            return {
                recommendations: [],
                loading: true,
            }
        },

        methods: {
            refreshRecommendations() {
                this.loading = true;
                this.recommendations = [];

                this.$http.post(this.API_URL + "/today_menu/recommended/?type=" + this.type).then((response) => {
                    this.loading = false;
                    this.recommendations = response.data;

                })
            }
        },

        mounted() {
            this.$http.get(this.API_URL + "/today_menu/recommended/?type=" + this.type).then(
                (response) => {
                    this.loading = false;
                    this.recommendations = response.data;

                }
            )
        }

    }
</script>