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
        <table class="table table-hover">
            <thead>
                <tr>
                    <th scope="col">Entity 1</th>
                    <th scope="col">Entity 2</th>
                    <th scope="col">Relation</th>
                    <th scope="col">Relation Score</th>
                    <th scope="col">Abstract</th>
                    <th scope="col">Article</th>
                    <th scope="col">Authors</th>
                    <th scope="col">Date</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(article, index) in results" :key="index">
                    <td>{{ article.closest_relation.e1 }}</td>
                    <td>{{ article.closest_relation.e2 }}</td>
                    <td>{{ article.closest_relation.relation }}</td>
                    <td>{{ article.relation_score }}</td>
                    <td>{{ article.sentences }}</td>
                    <td><a v-bind:href="'https://doi.org/'+ article.doi">{{ article.title }}</a></td>
                    <td>{{ article.authors }}</td>
                    <td>{{ article.date }}</td>
                </tr>
            </tbody>
        </table>
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
                console.log(response + " got response")
            }).catch((error) => {
                console.error(error);
            });
        },
    },
}
</script>
