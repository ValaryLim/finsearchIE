import Vue from 'vue';
import Router from 'vue-router';
import Search from '../components/Search.vue';
import About from '../components/About.vue';

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'About',
            component: About
        },
        {
            path: '/search',
            name: 'Search',
            component: Search,
        },
    ]
})