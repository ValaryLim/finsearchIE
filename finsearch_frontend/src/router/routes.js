import Vue from 'vue';
import Router from 'vue-router';
import SearchPage from '../components/SearchPage.vue';
import AboutPage from '../components/AboutPage.vue';

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'About',
            component: AboutPage
        },
        {
            path: '/search',
            name: 'Search',
            component: SearchPage,
        },
    ]
})