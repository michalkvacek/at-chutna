<template>
    <v-form @submit.prevent="login()" id="login-form">
        <v-alert type="error" class="error" :value="error">{{error}}</v-alert>

        <v-text-field prepend-icon="person" class="login-email" v-model="username" required label="E-mail"></v-text-field>
        <v-text-field prepend-icon="lock" class="login-password" v-model="password" required label="Heslo"
                      type="password"></v-text-field>

        <v-card-actions>
            <v-btn primary large block type="submit" form="login-form">Login</v-btn>

            <v-btn to="/zapomenute-heslo" secondary small flat>Zapomenuté heslo</v-btn>
        </v-card-actions>
    </v-form>
</template>


<script>
    export default {
        name: "login-form",
        data() {
            return {
                username: null,
                password: null,
                error: false,
            }
        },
        methods: {
            login: function () {
                let credentials = {
                    username: this.username,
                    password: this.password
                };

                this.$store.dispatch('loginUser', credentials).then(() => {
                    this.$router.push('/me-chute');
                }).catch((error) => {
                    for (let i in error.response.data) {
                        this.error = error.response.data[i][0];
                        break;
                    }
                });
            }
        }

    }
</script>