<template>
    <v-app class="overflow-hidden">
        <v-app-bar
            app
            color="primary" dark
            prominent dense
            scroll-target="#scrolling-techniques-3"
        >
        <v-app-bar-title class="text-no-wrap">
            <h4>
            <router-link to="/" tag="span" style="cursor: pointer">
                {{ title }}
            </router-link>
            </h4>
        </v-app-bar-title>
        <template v-slot:extension>
            <v-tabs align-with-title>
                <v-tab v-for="item in menu_items" :key="item.title" :to="item.path">
                    {{ item.title }}
                </v-tab>
            </v-tabs>
        </template>
        </v-app-bar>
        <v-sheet
            id="scrolling-techniques-3"
            class="overflow-y-auto"
        >
            <v-container style="height: 20px;"></v-container>
        </v-sheet>

        <v-content>
            <router-view></router-view>
        </v-content>
    </v-app>
</template>

<script>
export default {
    name: 'App',
    data() {
        return {
            title: 'FinSearch', 
            sidebar: false,
            menu_items: [
                { title: 'Search', path:'/' },
                { title: 'User Guide', path:'/userguide' },
                { title: 'About', path:'/about' },
            ]
        }
    }
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
}

.v-app-bar-title__content {
    width: 200px !important;
    margin-left: -22px;
}
</style>