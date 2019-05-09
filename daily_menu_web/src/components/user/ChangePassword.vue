<template>

    <v-form @submit.prevent="changePassword" id="change-password-form">
        <v-alert type="error" :value="!passwordsMatch">Ověření hesla nesouhlasí, zkuste to znovu.</v-alert>

        <v-alert type="success" :value="success">Heslo úspěšně změněno</v-alert>


        <v-text-field v-model="oldPassword" required label="Staré heslo" type="password"></v-text-field>
        <v-text-field v-model="newPassword" required label="Nové heslo" type="password"></v-text-field>
        <v-text-field v-model="newPasswordVerification" required label="Nové heslo (ověření)"
                      type="password"></v-text-field>

        <v-card-actions>
            <v-btn primary type="submit" form="change-password-form">Změnit heslo</v-btn>
        </v-card-actions>
    </v-form>

</template>

<script>

    export default {
        name: 'change-password',
        data() {
            return {
                oldPassword: null,
                newPassword: null,
                newPasswordVerification: null,
                passwordsMatch: true,
                success: false
            }
        },
        methods: {
            changePassword() {
                this.passwordsMatch = this.newPassword === this.newPasswordVerification;

                this.$http.put(this.API_URL + "/me/", {
                    password: this.newPassword,
                }).then(() => {
                    this.success = true
                }).catch(() => {
                    this.success = false
                })
            }
        }
    }
</script>