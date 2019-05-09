<template>
    <v-container fluid>
        <v-layout>
            <v-flex md9 xs12>
                <v-layout>
                    <v-flex xs12 class="mb-2" v-if="notUsed.length > 0">
                        <v-card class="mr-2">
                            <v-card-title primary-title="">
                                <h2>Přidejte svoji preferenci</h2>
                            </v-card-title>
                            <v-card-text>
                                <v-select
                                        :items="notUsed"
                                        label="Vyberte"
                                        item-name="text"
                                        item-value="key"
                                        class="preference-list-select"
                                        v-model="useClassification"
                                        @change="add"
                                        dense
                                ></v-select>
                            </v-card-text>
                        </v-card>
                    </v-flex>
                </v-layout>

                <v-layout wrap>

                    <v-flex xs12 sm4 md3 lg2 v-for="(preference, index) in used" class="preference-list-item"
                            :key="preference">
                        <v-card class="mr-2 mt-2">
                            <v-card-title>
                                <h3>{{availablePreferences[preference]}}</h3>
                            </v-card-title>

                            <v-card-text>
                                <v-radio-group v-model="preferences[preference]">
                                    <v-radio
                                            v-for="(value, index) in preferenceValues"
                                            :key="`${preference+'_'+index}`"
                                            :label="`${value}`"
                                            @change="save(preference, index)"
                                            :value=parseFloat(index)
                                    ></v-radio>
                                </v-radio-group>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn block small @click="remove(index)">Odebrat</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-flex>
                </v-layout>
            </v-flex>

            <v-flex md3 xs12>
                <daily-menu-mark-cousine></daily-menu-mark-cousine>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import DailyMenuMarkCousine from "../daily_menu/MarkCousine";

    export default {
        name: "user-taste",
        components: {DailyMenuMarkCousine},
        data() {
            return {
                useClassification: null,
                used: [],
                notUsed: [],
                preferences: {},

                preferenceValues: {
                    "1": "Mám rád/a",
                    "0.5": "Nevadí mi",
                    "-0.5": "Spíš mi nechutná",
                    "-1": "Nemám rád/a",
                },

                availablePreferences: {
                    "mushrooms": 'Houby',
                    'tofu': 'Tofu',
                    'vegetarian': 'Vegetariánské',
                    'pork': 'Vepřové maso',
                    "poultry": "Drůbeží maso",
                    "beef": "Hovězí maso",
                    'vegan': 'Veganské jídlo',
                    'meat': 'Maso obecně',
                    'venison': 'Divočina',
                    'fish': 'Ryby',
                    'seafood': 'Plody moře',
                    'pasta': 'Těstoviny',
                    'cheese': 'Sýry',
                    'mushroom': 'Houby',
                    'indian': 'Indická kuchyně',
                    'vietnamese': 'Vietnamská kuchyně',
                    'mexican': 'Mexická kuchyně',
                    'czech': 'Česká kuchyně',
                    'american': 'Americká kuchyně',
                    'japanese': 'Japonská kuchyně',
                    'chinese': 'Čínská kuchyně',
                    'italian': 'Italská kuchyně',
                    'soup': 'Polévky',
                    'sweet': 'Sladká jídla',
                },
            }
        },
        methods: {
            add() {
                this.used.unshift(this.useClassification);
                this.preferences[this.useClassification] = 0;

                let position = -1;
                for (let preference in this.notUsed) {
                    if (this.useClassification == this.notUsed[preference].key) {
                        position = preference;
                        break;
                    }
                }

                if (position >= 0)
                    this.notUsed.splice(position, 1);
                this.useClassification = null;

            },
            remove(index) {
                let item = this.used[index];

                this.used.splice(index, 1);
                this.notUsed.push({'key': item, 'text': this.availablePreferences[item]});
                this.preferences[item] = null;

                this.save(item, null);
            },
            save(preference, value) {
                this.$http.put(this.API_URL + '/me/preferences/', {
                    item: preference,
                    value: value
                });
            },
        },
        mounted() {
            this.$http.get(this.API_URL + "/me/preferences/").then((response) => {
                let data = response.data;
                let preferences = data;
                this.preferences = preferences;
                for (let preference in preferences) {
                    if (parseFloat(preferences[preference]) !== 0 && preferences[preference] != null) {
                        this.used.push(preference);
                    } else {
                        this.notUsed.push({"key": preference, 'text': this.availablePreferences[preference]});
                    }
                }
            });
        }
    }
</script>