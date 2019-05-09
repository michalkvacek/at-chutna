<template>

    <v-card>
        <v-card-title primary-title>
            <h2 class="headline">Pomozte nám s klasifikací</h2>
        </v-card-title>


        <v-card-text>

            <p>Přiřazením typické kuchyně k danému jídlu pomůžete zlepšit přesnost klasifikace denních menu. Díky tomu
                tak budete získávat přesnější a relevantnější doporučení.</p>


            <div v-for="menu in menus" :key="menu.id">

                <strong>{{menu.name}}</strong>
                <v-select
                        v-if="!rated[menu.id]"
                        :items="cousines"
                        label="Vyberte kuchyni"
                        item-name="text"
                        item-value="key"
                        v-model="classification[menu.id]"
                        @change="save(menu.id)"
                        dense
                ></v-select>

                <v-alert :value="error" type="error">
                    Při načítání došlo k chybě. Zkuste to prosím za chvíli znovu.
                </v-alert>


                <v-alert :value="rated[menu.id]" type="success">Děkujeme!</v-alert>
            </div>

            <v-alert type="info" :value="loading">Probíhá načítání...</v-alert>

            <v-btn @click="loadMenus" block small v-if="!loading ">Načíst jiná menu</v-btn>
        </v-card-text>
    </v-card>


</template>

<script>
    export default {
        name: "daily-menu-mark-cousine",

        data() {
            return {
                menus: [],
                rated: {},
                classification: {},
                loading: true,
                cousines: [
                    {key: 'sweet', text: 'Sladká jídla'},
                    {key: 'soup', text: 'Polévky'},
                    {key: 'indian', text: 'Indická kuchyně'},
                    {key: 'vietnamese', text: 'Vietnamská kuchyně'},
                    {key: 'mexican', text: 'Mexická kuchyně'},
                    {key: 'czech', text: 'Česká kuchyně'},
                    {key: 'american', text: 'Americká kuchyně'},
                    {key: 'chinese', text: 'Čínská kuchyně'},
                    {key: 'italian', text: 'Italská kuchyně'},
                    {key: 'japanese', text: 'Japonská kuchyně'},
                    {key: 'none', text: 'Ani jedno z vybraných'},
                ]
            }
        },

        methods: {
            save(menuId) {
                this.$http.put(this.API_URL + "/daily_menu/cousine/" + menuId + "/", {
                    cousine: this.classification[menuId]
                }).then((response) => {
                    this.saved = true;
                    this.rated[menuId] = true;

                    this.$set(this.rated, menuId, true)
                })
            },

            loadMenus() {
                this.$http.get(this.API_URL + "/daily_menu/cousine/").then((response) => {
                    this.error = this.loading = false;

                    this.menus = response.data.results;
                    this.classification = {};
                    this.rated = {};

                    for (let i in response.data.results) {
                        let meal = response.data.results[i];
                        this.classification[meal.id] = 0;
                        this.$set(this.rated, meal.id, false)
                    }
                }).catch(() => {
                    this.error = true;
                    this.loading = false;
                })
            }
        },
        mounted() {
            this.loadMenus()
        }

    }
</script>