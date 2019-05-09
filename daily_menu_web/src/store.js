import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

import settings from "./settings";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        authorization_token: null,
        user: null,
        watched_restaurants: []
    },
    mutations: {
        saveToken: (state, token) => {
            state.authorization_token = token;

            localStorage.authorizationToken = token;
        },
        saveUserInfo: (state, info) => {
            state.user = info;
        },
        logout: (state) => {
            state.authorization_token = null;
            delete localStorage.authorizationToken;
        },
        saveWatchedRestaurants: (state, restaurants) => {
            state.watched_restaurants = restaurants
        },
        watchRestaurant: (state, restaurant) => {
            let exists = false;
            for (let i in state.watched_restaurants) {
                if (state.watched_restaurants[i].id === restaurant.id) {
                    exists = true;
                    break;
                }
            }

            if (!exists)
                state.watched_restaurants.push(restaurant)
        },
        unwatchRestaurant: (state, restaurant) => {
            let position = -1;

            // find position of given restaurant
            for (let i in state.watched_restaurants) {
                if (state.watched_restaurants[i].id === restaurant.id) {
                    position = i;
                    break;
                }
            }

            if (position >= 0) {
                state.watched_restaurants.splice(position, 1);
            }
        }
    },

    getters: {
        getAuthToken: (state) => {
            if (state.authorization_token === null) {
                state.authorization_token = localStorage.getItem('authorizationToken');
            }

            return state.authorization_token;
        },
        isLoggedIn: (state, getters) => {
            return getters.getAuthToken !== null
        },
        isRestaurantWatched: (state) =>
            (restaurant) => {
                // find position of given restaurant
                for (let i in state.watched_restaurants) {
                    if (state.watched_restaurants[i].id === restaurant.id) {
                        return true;
                    }
                }
                return false;
            }
    },

    actions: {
        loginUser: ({commit, dispatch}, credentials) => {
            return axios.post(settings.API_URL + '/login/', credentials).then((response) => {
                commit('saveToken', response.data.token);
                dispatch('loadUserInfo');

            })
        },

        loadWatchedRestaurants: ({commit}) => {
            return axios.get(settings.API_URL + '/restaurants/watched/').then((response) => {
                // console.log(response.data);
                commit('saveWatchedRestaurants', response.data)
            })
        },

        loadUserInfo: ({commit, getters, dispatch}) => {
            if (!getters.isLoggedIn)
                return;

            return axios.get(settings.API_URL + "/me/").then((response) => {
                commit('saveUserInfo', response.data);
                dispatch('loadWatchedRestaurants');
            }).catch(() => {
                // error occured, fire logout
                commit('logout');
                commit('saveUserInfo', {});
                commit('saveWatchedRestaurants', []);
            })
        },

        updateUserInfo: ({commit}, data) => {
            return axios.put(settings.API_URL + '/me/', data).then((response) => {
                commit('saveUserInfo', response.data)
            })
        }

    }
})
