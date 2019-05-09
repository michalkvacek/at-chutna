<template>
    <v-dialog
            v-model="dialog"
            width="500">

        <template v-slot:activator="{ on }">
            <v-btn block v-on="on">
                Zobrazit více
            </v-btn>
        </template>

        <v-card>
            <v-card-title
                    class="headline grey lighten-2"
                    primary-title>
                Denní menu
            </v-card-title>

            <v-card-text>
                <daily-menu v-for="menu in list" :key="menu.id" :menu="menu"></daily-menu>
            </v-card-text>

            <v-divider></v-divider>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary"
                       flat
                       @click="dialog = false">
                    Zavřít
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import DailyMenu from "./DailyMenu";

    export default {
        name: "long-daily-menu-list",
        components: {DailyMenu},
        props: ['list'],
        data() {
            return {
                dialog: false
            }
        }
    }
</script>