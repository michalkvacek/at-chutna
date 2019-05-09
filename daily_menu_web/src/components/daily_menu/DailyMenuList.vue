<template>
    <div>
        <daily-menu v-for="menu in max > 0 ? list.slice(0, max) : list" :key="menu.id" :menu="menu"></daily-menu>

        <div v-if="max > 0 && list.length > max">
            <long-daily-menu-list :list="list"></long-daily-menu-list>
        </div>

        <v-alert type="info"
                 outline
                 :value="list.length === 0">
            Na dnešek nebylo vypsáno denní menu
        </v-alert>
    </div>
</template>

<script>
    import DailyMenu from "./DailyMenu";
    import LongDailyMenuList from "./LongDailyMenuList";

    export default {
        name: 'daily-menu-list',
        props: {
            list: {
                default: [],
                type: Array
            },
            max: {
                default: 3,
                type: Number
            }
        },
        components: {
            LongDailyMenuList,
            DailyMenu
        },
        watch: {
            list: {
                immediate: true,
                handler: function (oldVal, newVal) {
                    for (let i in this.list) {
                        let rating = this.list[i].rating;
                        if (typeof rating !== 'undefined' && rating.length > 0) {
                            if (!rating[0].is_meal) {
                                this.list.splice(i  , 1);
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
</script>