<template>
    <v-layout justify-center>
        <vue-title title="Vyhledávání"></vue-title>


        <v-flex md11>
            <v-card>
                <v-card-title primary-title>
                    <h1>Vyhledávání</h1>
                </v-card-title>
                <v-card-text>

                    <search></search>

                </v-card-text>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import Search from "../components/daily_menu/Search";

    export default {
        components: {Search}
    }
</script>
