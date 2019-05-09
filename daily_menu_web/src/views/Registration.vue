<template>
<v-layout justify-center align-center>
    <vue-title title="Registrace"></vue-title>
        <v-flex md4>

            <v-card flat>
                <v-card-title primary-title>
                    <h3 class="headline mb-0">Nový účet</h3>
                </v-card-title>

                <registration-form></registration-form>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>

    import RegistrationForm from "../components/auth/RegisterForm";
    export default {
        components: {RegistrationForm}
    }
</script>