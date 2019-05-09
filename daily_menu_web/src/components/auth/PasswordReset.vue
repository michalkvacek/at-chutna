<template>
    <v-form @submit.prevent="reset()" id="reset-password-form">
        <v-alert type="error" :value="error !== false">{{error}}</v-alert>

        <v-alert type="success" :value="success">E-mail s novým heslem byl odeslán na e-mail.</v-alert>

        <v-alert type="info" :value="sending">Probíhá odesílání e-mailu</v-alert>

        <v-text-field prepend-icon="person" name="E-mail" v-model="email" type="email" required
                      label="E-mail"></v-text-field>

        <v-card-actions>

            <v-btn primary large block type="submit" form="reset-password-form">Resetovat heslo</v-btn>

            <v-btn to="/prihlaseni" secondary small flat>Zpět na přihlášení</v-btn>
        </v-card-actions>
    </v-form>
</template>

<script>
    export default {
        name: 'password-reset-form',

        data() {
            return {
                email: null,
                error: false,
                success: false,
                sending: false
            }
        },

        methods: {
            reset() {
                this.sending = true
                this.$http.post(this.API_URL + "/reset_password", {
                    email: this.email
                }).then(() => {
                    this.success = true;
                    this.error = false;
                    this.sending = false;
                }).catch((error) => {

                    this.success = false;
                    this.sending = false;

                    for (let i in error.response.data) {
                        this.error = error.response.data[i][0];
                        break;
                    }
                });
            }
        }
    }
</script>