<template>
    <v-layout justify-center align-center>
        <vue-title title="Přihlášení"></vue-title>

        <v-flex md4>

            <v-card flat>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Login</h3>
                </v-card-title>
                <login-form></login-form>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import LoginForm from "../components/auth/LoginForm";

    export default {
        name: "login",
        components: {LoginForm}
    }
</script>