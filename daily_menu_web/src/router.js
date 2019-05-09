import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import RestaurantDetail from "./views/RestaurantDetail";
import Login from "./views/Login"
import Profile from "./views/profile/Profile";
import Search from "./views/Search";
import Preferences from "./views/profile/Preferences";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
            meta: {requiresAuth: false},
        },

        {
            path: '/vyhledavani',
            name: 'search',
            component: Search,
            meta: {requiresAuth: false},
        },

        {
            path: '/restaurace/:id',
            name: 'restaurant_detail',
            component: RestaurantDetail,
            meta: {requiresAuth: false}
        },

        {
            path: '/prihlaseni',
            name: 'login',
            component: Login,
            meta: {requiresAuth: false}
        },

        {
            path: '/zapomenute-heslo',
            name: 'password_reset',
            component: () => import('./views/PasswordReset.vue'),
            meta: {requiresAuth: false}
        },

        {
            path: '/registrace',
            name: 'registration',
            component: () => import('./views/Registration.vue'),
            meta: {requiresAuth: false}
        },

        {
            path: '/o-projektu',
            name: 'about',
            component: () => import('./views/About.vue'),
            meta: {requiresAuth: false}
        },
        {
            path: '/sledovane',
            name: 'profile',
            component: Profile,
            meta: {requiresAuth: true}
        },
        {
            path: '/spolecny-obed',
            name: 'friends',
            component: () => import('./views/profile/Friends.vue'),
            meta: {requiresAuth: true}
        },
        {
            path: '/osobni-udaje',
            name: 'personal',
            component: () => import('./views/profile/Personal.vue'),
            meta: {requiresAuth: true}
        },
        {
            path: '/me-chute',
            name: 'preferences',
            component: Preferences,
            meta: {requiresAuth: true}
        }


    ]
})
