<template>

    <v-layout justify-center>

        <vue-title title="Mé chutě"></vue-title>


        <div>
            <map-with-location-input type="personal">
                Vyberte, z jakých míst chcete dostávat doporučení.
            </map-with-location-input>
            <user-taste></user-taste>
        </div>
    </v-layout>

</template>

<script>
    import PersonalSettings from "../../components/user/PersonalSettings";
    import ChangePassword from "../../components/user/ChangePassword";
    import UserTaste from "../../components/user/UserTaste";
    import MapWithLocationInput from "../../components/user/UserLocationInput";

    export default {
        data() {
            return {
                show: false
            }
        },
        components: {MapWithLocationInput, UserTaste, ChangePassword, PersonalSettings}
    }
</script>


