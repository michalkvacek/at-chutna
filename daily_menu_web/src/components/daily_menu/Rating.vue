<template>
    <v-select
            v-if="!rated"
            :items="values"
            label="Ohodnotit"
            item-name="text"
            item-value="key"
            v-model="rating"
            class="daily-menu-rating"
            @change="rateMenu"
            dense
    ></v-select>

    <v-alert outline type="success" v-else :value="ratedNow">Díky za reakci!</v-alert>
</template>

<style lang="scss" scoped>
    .v-input {
        display: inline;
    }
</style>

<script>
    export default {
        name: "daily-menu-rating",
        props: ['menu'],
        data() {
            return {
                values: [
                    {key: 'had_liked', text: 'Chutnalo mi'},
                    {key: 'not_had_liked', text: 'Dal/a bych si'},
                    {key: 'had_not_liked', text: 'Nechutnalo mi'},
                    {key: 'not_had_not_liked', text: 'Nedal/a bych si'},
                    {key: 'not_meal', text: 'Toto není jídlo'},

                ],
                rating: 0,
                rated: false,
                ratedNow: false
            }
        },
        mounted() {
            if (this.menu.rating.length > 0) {
                this.rated = true;
            }
        },

        methods: {
            rateMenu() {

                let had, liked, meal;
                switch (this.rating) {
                    case 'had_liked':
                        meal = had = liked = true;
                        break;
                    case 'had_not_liked':
                        meal = true;
                        had = true;
                        liked = false;
                        break;
                    case 'not_had_liked':
                        meal = true;
                        had = false;
                        liked = true;
                        break;
                    case 'not_had_not_liked':
                        meal = true;
                        had = liked = false;
                        break;
                    case 'not_meal':
                        meal = had = liked = false;
                        break;
                }

                this.$http.post(this.API_URL + "/daily_menu/rating/", {
                    rating: this.rating,
                    daily_menu: this.menu.id,
                    had: had,
                    liked: liked,
                    is_meal: meal,
                }).then(() => {
                    this.rated = true;
                    this.ratedNow = true;
                }).catch(() => {
                })

            }
        }
    }
</script>