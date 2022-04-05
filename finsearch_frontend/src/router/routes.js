import Vue from 'vue';
import Router from 'vue-router';
import SearchPage from '../components/SearchPage.vue';
import AboutPage from '../components/AboutPage.vue';
import UserGuidePage from '../components/UserGuidePage.vue';

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'Search',
            component: SearchPage
        },
        {
            path: '/userguide',
            name: 'User Guide',
            component: UserGuidePage
        },
        {
            path: '/about',
            name: 'About',
            component: AboutPage,
        },
    ]
})