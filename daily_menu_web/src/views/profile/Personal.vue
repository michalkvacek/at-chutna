<template>

    <v-layout justify-center>

        <vue-title title="Osobní nastavení"></vue-title>

        <v-flex md6 class="mr-2">
            <v-card>
                <v-card-title>
                    <h2>Osobní nastavení</h2>
                </v-card-title>

                <v-card-text>
                    <personal-settings></personal-settings>
                </v-card-text>
            </v-card>
        </v-flex>

        <v-flex md6 class="ml-2">
            <v-card>
                <v-card-title>
                    <h2>Změna hesla</h2>
                </v-card-title>

                <v-card-text>
                    <change-password></change-password>
                </v-card-text>
            </v-card>
        </v-flex>
    </v-layout>

</template>

<script>
    import PersonalSettings from "../../components/user/PersonalSettings";
    import ChangePassword from "../../components/user/ChangePassword";

    export default {
        components: {ChangePassword, PersonalSettings}
    }
</script>


