<template>
    <v-app>

        <v-toolbar dark app color="#007d00" flat>
            <router-link to="/" tag="v-toolbar-title">AťChutná.cz</router-link>

            <v-spacer></v-spacer>
            <v-toolbar-items class="hidden-sm-and-down">
                <v-btn
                        v-for="item in menu"
                        :key="item.link"
                        :to="item.link"
                        exact
                        flat
                >{{ item.title }}
                </v-btn>

                <v-btn v-if="isLoggedIn" flat @click.prevent="logout">Odhlásit</v-btn>

            </v-toolbar-items>
            <v-menu class="hidden-md-and-up">
                <v-toolbar-side-icon slot="activator"></v-toolbar-side-icon>
                <v-list>
                    <v-list-tile v-for="item in menu" :key="item.link">
                        <v-list-tile-content>

                            <router-link :to="item.link">
                                {{ item.title }}
                            </router-link>

                        </v-list-tile-content>
                    </v-list-tile>

                    <v-list-tile>
                        <v-list-tile-content>
                            <a v-if="isLoggedIn" flat @click.prevent="logout">Odhlásit</a>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>
            </v-menu>
        </v-toolbar>


        <v-content>
            <v-container fluid>
                <router-view></router-view>
            </v-container>
        </v-content>
<!--        <v-footer app>-->
<!--            <v-spacer></v-spacer>-->
<!--            <router-link to="/about">O projektu</router-link>-->

<!--        </v-footer>-->
    </v-app>

</template>

<style lang="scss">
    * {
        max-width: 100%;
    }

    // info taky zelene

    .v-toolbar {
        a {
            color: white !important;
        }
    }

    .v-toolbar:hover {
        cursor: pointer;
    }

    .theme--light.application {
        /*color: #007d00;*/
        background: #ddd !important;
    }

    a {
        color: green !important;
        text-decoration: none;
        font-weight: bold;

        &:hover {
            text-decoration: underline;
        }
    }
</style>

<script>
    import {mapGetters} from 'vuex'

    export default {
        data() {
            return {
                menu: [],
                loggedMenu: [
                    {title: 'Vyhledávání', link: '/vyhledavani'},
                    {link: "/me-chute", title: "Mé chutě"},
                    {link: "/sledovane", title: "Sledované"},
                    {link: "/spolecny-obed", title: "Společný oběd"},
                    {link: "/osobni-udaje", title: "Nastavení"},
                ],
                notLoggedMenu: [
                    {title: 'Vyhledávání', link: '/vyhledavani'},
                    {title: 'Přihlášení', link: '/prihlaseni'},
                    {title: 'Registrace', link: '/registrace'},
                ],
            }
        },
        computed: {
            ...mapGetters(['isLoggedIn'])
        },
        watch: {
            isLoggedIn: {
                immediate: true,
                handler: function () {
                    if (this.isLoggedIn) {
                        this.menu = this.loggedMenu;
                    } else {
                        this.menu = this.notLoggedMenu
                    }
                }
            }
        },
        methods: {
            menuItems() {
                return this.menu
            },
            logout: function () {
                this.$store.commit('logout');
                this.$router.push('/');
            }
        },
        mounted() {
            this.$store.dispatch('loadUserInfo')
        }
    }
</script>