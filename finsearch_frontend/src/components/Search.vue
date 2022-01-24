<template>
  <div class="search">
    <b-form @submit="submit">
        <b-input-group prepend="Entity 1" class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input id="entity1" class="mb-2 mr-sm-2 mb-sm-0" type="text" placeholder="economic growth" v-model="form.entity1" required></b-form-input>
        </b-input-group>
        <br>
        <b-input-group prepend="Entity 2" class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input id="entity2" type="text" placeholder="interest rates" v-model="form.entity2" required></b-form-input>
        </b-input-group>
        <br>
        <b-button id="submit" variant="dark" type="submit">Search</b-button>
    </b-form>
    <br>
    <div id="entity-display">
        <p>Entity 1: {{ form.entity1 }}</p>
        <p>Entity 2: {{ form.entity2 }}</p>
    </div>
    <br>

    <div id="results">
        <h3>Results</h3>
        <p>{{ results }}</p>
    </div>

    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Search',
    data() {
        return {
            form: {
                entity1: '',
                entity2: ''
            },
            results: {},
        }
    },
    props: {
        msg: String
    },
    methods: {
        submit(event) {
            event.preventDefault();
            const path = 'http://127.0.0.1:5000/search';
            const search_query = {
                entity1: this.form.entity1,
                entity2: this.form.entity2,
            };
            axios.post(path, search_query).then(response => {
                this.results = response.data.results
            }).catch((error) => {
                console.error(error);
            });
        },
    },
}
</script>