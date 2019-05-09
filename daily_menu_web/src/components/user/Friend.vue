<template>
    <div class="friend">
        <v-avatar
                size="80"
                color="grey lighten-4">
            <img :src="friendship.friend.avatar" alt="avatar">
        </v-avatar>

        <v-layout justify-center>
            <v-checkbox
                    v-model="together"
                    @change="changeLunch"
                    style="max-width: 200px"
                    label="Jít na společný oběd"></v-checkbox>
        </v-layout>
        <strong v-if="friendship.friend.first_name !== '' || friendship.friend.last_name !== ''">
            {{friendship.friend.first_name}} {{friendship.friend.last_name[0]}}.
        </strong>

        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "friendship",
        props: ['friendship'],
        data() {
            return {
                together: true
            }
        },
        methods: {
            changeLunch() {
                this.$http.put(this.API_URL + '/me/friends/' + this.friendship.id + '/', {
                    lunch_together: this.together
                });
            }
        },
        mounted() {
            this.together = this.friendship.lunch_together;
        }
    }
</script>