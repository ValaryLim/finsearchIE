<template>
  <div class="search">
    <v-app id="search">
        <div id="form">
        <v-form @submit="submit" v-model="form.valid">
            <v-container>
                <v-row>
                    <v-col cols="12" md="6">
                        <v-text-field
                            v-model="form.entity1"
                            :rules="form.rules.required"
                            color="primary"
                            label="Entity 1"
                            placeholder="Economic growth"
                            type="text"
                        ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="6">
                        <v-text-field
                            v-model="form.entity2"
                            :rules="form.rules.required"
                            color="primary"
                            label="Entity 2"
                            placeholder="Interest rates"
                            type="text"
                        ></v-text-field>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12" md="4">
                        <v-slider
                            v-model="form.threshold"
                            step="0.1"
                            ticks="always"
                            tick-size="5" thumb-label
                            min="0" max="1"
                            :label="'Threshold'"
                        >
                            <template v-slot:append>
                            <v-text-field
                                v-model="form.threshold"
                                class="mt-0 mb-0 pt-0"
                                type="number"
                                style="width:50px"
                            ></v-text-field>
                            </template>
                        </v-slider>
                    </v-col>
                    <v-col cols="12" md="1"></v-col>
                    <v-col cols="12" md="2">
                        <v-switch 
                            inset color="primary" 
                            v-model="form.direction" 
                            :label="directionToggle()"
                            class="mt-0 pt-0"
                        ></v-switch>
                    </v-col>
                    <v-col cols="12" md="2">
                        <v-switch 
                            inset color="primary" 
                            v-model="form.granular" 
                            :label="granularToggle()"
                            class="mt-0 pt-0"
                        ></v-switch>
                    </v-col>
                    <v-col cols="12" md="3"></v-col>
                </v-row>
                <v-row>
                    <v-btn id="submit" :disabled="!form.valid" type="submit" color="primary" elevation="2" large rounded>
                        Search
                    </v-btn>
                </v-row>
            </v-container>
        </v-form>
        </div>
        <br>
        <br>
        <br>

        <div id="results">
            <!-- add date filtering, add relation score -->
            <v-container>
                <v-row>
                    <h4>Finsearch Results</h4>
                </v-row>
                <v-row align="center">
                    <v-col cols="12" xl="9" lg="8" md="7" sm="0"></v-col>
                    <v-col cols="12" xl="3" lg="4" md="5" sm="12">
                        <v-select 
                            v-model="filtered_relations.granular"
                            :items="relations.granular"
                            filled chips label="Relations Filter" multiple>
                            <template v-slot:selection="{ item, index }">
                                <v-chip v-if="index < 2" color="primary">
                                    <span>{{ item }}</span>
                                </v-chip>
                                <v-chip v-if="index === 2">
                                    <span>+{{ filtered_relations.granular.length - 2 }} Others</span>
                                </v-chip>
                            </template>
                        </v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-data-table 
                        :headers="headers" 
                        :items="Object.values(results)" 
                        :items-per-page="10" 
                        class= "elevation-1" 
                        :loading = "loading"
                        loading-text = "Retrieving results..."
                    >  
                        <template v-slot:item.relation_score="{ item }">
                            {{ displayRelationScore(item.relation_score )}}
                        </template>
                        <template v-slot:item.sentences="{ item }">
                            {{ processAbstract(item.sentences, item.relations) }}
                        </template>
                        <template v-slot:item.title="{ item }">
                            <a :href="'https://doi.org/' + item.doi">{{ item.title }}</a>
                        </template>
                        <!-- <template v-slot:item.authors="{ item }">
                            <p class="author" v-for="(author, index) in item.authors" :key=index>
                                {{ author }}
                            </p>
                        </template> -->
                    </v-data-table>
                </v-row>
            </v-container>
            
                    </div>
    </v-app>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Search',
    data() {
        return {
            switch1: false,
            loading : false,
            form: {
                valid:false,
                rules: {
                    required: [value => !!value || "Required."]
                },
                entity1: '',
                entity2: '',
                direction: true,
                threshold: 0.5,
                granular: true
            },
            results: {},
            headers: [
                { text: 'Entity 1', align: 'left', value: 'closest_relation.e1', width:'10%' },
                { text: 'Entity 2', value: 'closest_relation.e2', width:'10%' },
                { text: 'Relation', value: 'closest_relation.relation', align: 'center', width:'6%' },
                { text: 'Relation Score', value: 'relation_score', align: 'center', width:'6%' },
                { text: 'Abstract', value: 'sentences', width:'43%' },
                { text: 'Title', value: 'title', width: '15%' },
                { text: 'Date', value: 'date', width: '10%' },
            ],
            filtered_relations: {
                granular: [  'ATTRIBUTE', 'FUNCTION', 'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'NONE', 'CONDITION', 'COMPARISON', 'UNCERTAIN' ]
            },
            relations: {
                coarse: [ 'DIRECT', 'INDIRECT' ],
                granular: [  'ATTRIBUTE', 'FUNCTION', 'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'NONE', 'CONDITION', 'COMPARISON', 'UNCERTAIN' ]
            },
            desserts: [
                { title: ['test.', 'test'],  'date': 'dATE DATE' }
            ]
        }
    },
    props: {
        msg: String
    },
    methods: {
        submit(event) {
            this.loading = true
            event.preventDefault();
            const path = 'http://127.0.0.1:5000/search';
            const search_query = {
                entity1: this.form.entity1,
                entity2: this.form.entity2,
                direction: this.form.direction,
                threshold: this.form.threshold,
                granular: this.form.granular
            }
            axios.post(path, search_query).then(response => {
                this.results = response.data.results
            }).catch((error) => {
                console.error(error)
            })
            this.loading = false
        },
        directionToggle() {
            if (this.form.direction) {
                return "Ordered"
            } else {
                return "Interchangeable Order"
            }
        },
        granularToggle() {
            if (this.form.granular) {
                return "Granular Relations"
            } else {
                return "Coarse Relations"
            }
        },
        displayRelationScore(score) {
            return (score * 100).toFixed(0)
        },
        processAbstract(sentences, relations) {
            console.log(sentences)
            console.log(relations)
            return sentences.join(' ')
        },
        relationFilterOptions() {
            if (this.form.granular) {
                return this.relations.granular
            } else {
                return this.relations.coarse
            }
        }
    },
}
</script>

<style>
.v-form {
    white-space: nowrap;
}

td {
  text-align: center !important;
}


.author {
    line-height: 95%;
    white-space: nowrap;
}
</style>