import Vue from 'vue'

import axios from 'axios'
import router from './router'
import store from './store'
import settings from "./settings"
import App from './App.vue'

import * as VueGoogleMaps from "vue2-google-maps";

import './plugins/vuetify'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'

import titleComponent from './components/PageTitle';
Vue.component('vue-title', titleComponent);

Vue.use(Vuetify);

import VueGeolocation from 'vue-browser-geolocation';

Vue.use(VueGeolocation);

Vue.use(VueGoogleMaps, {
    load: {
        key: settings.GOOGLE_MAPS_API_KEY
    }
});


Vue.config.productionTip = false;

router.beforeEach((to, from, next) => {

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.getters.isLoggedIn) {
            next({
                path: '/login',
                query: {redirect: to.fullPath}
            })
        } else {
            next()
        }
    } else {
        next()
    }
});

axios.interceptors.request.use(
    (config) => {
        let token = store.getters.getAuthToken;

        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }

        return config;
    },

    (error) => {
        return Promise.reject(error);
    }
);

Vue.prototype.$http = axios;
Vue.prototype.API_URL = settings.API_URL;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');