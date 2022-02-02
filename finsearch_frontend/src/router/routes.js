import Vue from 'vue';
import Router from 'vue-router';
import Search from '../components/Search.vue';
import HelloWorld from '../components/HelloWorld.vue';

Vue.use(Router)

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'HelloWorld',
            component: HelloWorld,
        },
        {
            path: '/search',
            name: 'Search',
            component: Search,
        },
    ]
})