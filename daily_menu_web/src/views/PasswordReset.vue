<template>
    <v-layout justify-center align-center>
        <vue-title title="Reset hesla"></vue-title>

        <v-flex md4>

            <v-card flat>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Zapomenuté heslo</h3>
                </v-card-title>
                <password-reset-form></password-reset-form>
            </v-card>
        </v-flex>
    </v-layout>
</template>
<script>
    import PasswordResetForm from "../components/auth/PasswordReset";
    export default {
        components: {PasswordResetForm}
    }
</script>