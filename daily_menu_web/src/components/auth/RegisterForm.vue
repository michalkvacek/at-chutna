<template>
    <v-form @submit.prevent="register" id="register-form">
        <v-alert type="error" :value="error">{{error}}</v-alert>

        <v-text-field prepend-icon="email" class="register-email" v-model="email" required label="E-mail"></v-text-field>
        <v-text-field prepend-icon="lock" class="register-password" name="Heslo" v-model="password" required label="Heslo"
                      type="password"></v-text-field>

        <v-card-actions>
            <v-btn primary large block type="submit" form="register-form">Registrovat</v-btn>
        </v-card-actions>
    </v-form>
</template>


<script>
    export default {
        name: "registration-form",
        data() {
            return {
                email: null,
                password: null,
                error: false
            }
        },
        methods: {
            register: function () {
                this.$http.post(this.API_URL + "/registration/", {
                    first_name: '',
                    last_name: '',
                    password: this.password,
                    email: this.email,
                    username: this.email,
                }).then(() => {
                    this.error = false;

                    // login user after successful registration
                    this.$store.dispatch('loginUser', {
                        username: this.email,
                        password: this.password
                    }).then(() => {
                        this.$router.push('/me-chute');
                    })
                }).catch(
                    (error) => {

                        for (let i in error.response.data) {
                            this.error = error.response.data[i][0];
                            break;
                        }

                    }
                )
            }
        }
    }
</script>