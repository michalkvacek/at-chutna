<template>

    <v-form @submit.prevent="save" id="personal-settings-form">

        <v-alert type="success" :value="success">Úspěšně uloženo</v-alert>

        <v-text-field v-model="first_name" required label="Jméno"></v-text-field>
        <v-text-field v-model="last_name" required label="Příjmení"></v-text-field>

        <v-card-actions>
            <v-btn primary type="submit" form="personal-settings-form">Uložit</v-btn>
        </v-card-actions>
    </v-form>
</template>

<script>
    export default {
        name: "personal-settings",

        data() {
            return {
                first_name_save: '',
                last_name_save: '',
                success: false
            }
        },

        computed: {
            first_name: {
                get() {
                    return this.$store.state.user ? this.$store.state.user.first_name : ''
                },
                set(value) {
                    this.first_name_save = value;
                }
            },
            last_name: {
                get() {
                    return this.$store.state.user ? this.$store.state.user.last_name : ''
                },
                set(value) {
                    this.last_name_save = value;
                }
            }
        },
        methods: {
            save() {
                this.$store.dispatch('updateUserInfo', {
                    first_name: this.first_name_save,
                    last_name: this.last_name_save
                }).then(() => {
                    this.success = true;
                })
            }
        },
    }
</script>