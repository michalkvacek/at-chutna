<template>
    <div>
        <vue-title title="Seznam přátel"></vue-title>

        <recommended-daily-menus v-if="friends.length > 0" type="friends"></recommended-daily-menus>

        <map-with-location-input type="friends">
            Vyberte místo, kde chcete jít s přáteli na oběd.
        </map-with-location-input>

        <v-container fluid>
            <v-flex>
                <v-card>
                    <v-card-title>
                        <div>
                            <h3>Přátelé</h3>

                            Přidejte si sem své přátelé a nechte si doporučovat restaurace pro společný oběd.
                        </div>
                    </v-card-title>
                    <v-card-text>
                        <v-layout row wrap class="friendship-list">
                            <v-flex justify-center class="friendship text-xs-center"
                                    v-for="(friendship, index) in friends"
                                    :key="index">

                                <friend :friendship="friendship">
                                    <v-btn flat small class="remove-friend" @click="remove(friendship, index)">
                                        Odebrat
                                    </v-btn>
                                </friend>

                            </v-flex>
                        </v-layout>

                        <v-alert type="info" outline :value="friends.length === 0">
                            Aktuálně nemáte žádné přátele. Přidejte si sem své kolegy a získavejte společná doporučení.
                        </v-alert>

                    </v-card-text>
                </v-card>

                <v-card class="mt-3">
                    <v-card-title>
                        <h3>Přidejte přítele</h3>
                    </v-card-title>
                    <v-card-text>

                        <v-form @submit.prevent="addFriend()" id="search-friend-form">

                            <v-alert type="error" :value="userNotFound">
                                Uživatel s e-mailem {{searchEmail}} nenalezen.
                            </v-alert>

                            <v-alert type="error" :value="alreadyExists">
                                Tento uživatel již je tvůj kamarád.
                            </v-alert>

                            <v-alert type="error" :value="addOwn">
                                Nelze přidat svůj profil.
                            </v-alert>

                            <v-text-field prepend-icon="person"
                                          name="E-mail"
                                          class="friend-email"
                                          @keydown="userNotFound = false"
                                          v-model="searchEmail" required
                                          label="E-mail"></v-text-field>


                            <v-btn primary large block type="submit" form="search-friend-form">Najít a přidat</v-btn>

                        </v-form>

                    </v-card-text>
                </v-card>
            </v-flex>

            <v-flex lg4>
            </v-flex>
        </v-container>
    </div>

</template>


<script>
    import MapWithLocationInput from "../../components/user/UserLocationInput";
    import Friend from "../../components/user/Friend";
    import RecommendedDailyMenus from "../../components/daily_menu/RecommendationList";

    export default {
        components: {RecommendedDailyMenus, Friend, MapWithLocationInput},
        data() {
            return {
                searchEmail: null,
                loading: true,
                userNotFound: false,
                alreadyExists: false,
                addOwn: false,
                friends: []
            }
        },
        methods: {
            hideErrors() {
                this.userNotFound = false;
            },

            loadFriends() {
                this.$http.get(this.API_URL + '/me/friends/').then((response) => {
                    this.friends = response.data;
                    this.loading = false;
                });
            },
            remove(friend, index) {
                this.$http.delete(this.API_URL + '/me/friends/' + friend.id).then(() => {
                    this.friends.splice(index, 1)
                })
            },
            addFriend() {
                this.addOwn = this.userNotFound = this.alreadyExists = false;

                if (this.searchEmail === this.$store.state.user.email) {
                    this.addOwn = true;
                    return;
                }

                this.$http.post(this.API_URL + "/me/friends/", {
                    email: this.searchEmail
                }).then(
                    () => {
                        this.userNotFound = false;
                        this.searchEmail = null;
                        this.loadFriends()
                    }
                ).catch((error) => {


                    if (error.response.status === 404) {
                        this.userNotFound = true;
                    } else if (error.response.status === 409) {
                        this.alreadyExists = true;
                    }
                })
            }
        },
        mounted() {
            this.loadFriends();
        }
    }
</script>