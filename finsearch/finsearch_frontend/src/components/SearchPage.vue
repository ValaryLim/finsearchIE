<template>
    <div class="search">
        <v-container fluid>
            <v-layout row wrap>
            <v-flex xs12 class="text-xs-center" mt-5>
                <h2>FinSearch</h2>
                <p>
                    Use the form below to retrieve a table of abstracts relevant to your two searched entities. 
                    Refer to the User Guide for more information on the form options.
                </p>
            </v-flex>
            </v-layout>
        </v-container>
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
                        <v-col cols="12" md="12" lg="4">
                            <v-slider
                                v-model="form.threshold"
                                step="10"
                                ticks="always"
                                tick-size="5" thumb-label
                                min="0" max="100"
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
                        <v-col class="hidden-sm-and-down" cols="12" md="1"></v-col>
                        <v-col cols="12" md="4" lg="3">
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
                        <v-col cols="12" md="6" lg="4">
                            <v-select
                            :label="'Model'"
                            :items="form.model_options"
                            v-model="form.model"
                            dense
                            ></v-select>
                        </v-col>
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
        <div id="results">
            <v-container>
                <v-row>
                    <h5>Search Results</h5>
                </v-row>
                <v-row align="center">
                    <v-col cols="12" xl="8" lg="7" md="5" sm="0"></v-col>
                    <v-col cols="12" xl="4" lg="5" md="7" sm="12">
                        <v-select 
                            v-model="relation_labels.selected"
                            :items="relationFilterOptions()"
                            filled chips label="Relations Filter" multiple>
                            <template v-slot:[`selection`]="{ item, index }">
                                <v-chip v-if="index < 2" color="primary">
                                    <span>{{ item }}</span>
                                </v-chip>
                                <v-chip v-if="index === 2" style="background-color:white;">
                                    <span>+{{ relation_labels.selected.length - 2 }} Others</span>
                                </v-chip>
                            </template>
                        </v-select>
                    </v-col>
                </v-row>
                <v-row>
                    <v-data-table 
                        :headers="display.headers" 
                        :items="relationFilter()" 
                        :items-per-page="10" 
                        class="elevation-1" 
                        :loading="display.loading"
                        loading-text="Retrieving results..."
                        :sort-by.sync="display.sort_by"
                        :sort-desc.sync="display.sort_desc"
                    > 
                        <template v-slot:[`item.closest_relation.e1`]="{ item }">
                            <span class='entity entity1'>{{ item.closest_relation.e1 }}</span>
                        </template>
                        <template v-slot:[`item.closest_relation.e2`]="{ item }">
                            <span class='entity entity2'>{{ item.closest_relation.e2 }}</span>
                        </template>
                        <template v-slot:[`item.relation_score`]="{ item }">
                            {{ displayRelationScore(item.relation_score )}}
                        </template>
                        <template v-slot:[`item.sentences`]="{ item }">
                            <div v-html="displayAbstract(item.sentences, item.closest_relation)"></div>
                            
                        </template>
                        <template v-slot:[`item.title`]="{ item }">
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
    name: 'SearchPage',
    data() {
        return {
            form: {
                valid:false,
                rules: {
                    required: [value => !!value || "Required."]
                },
                entity1: '',
                entity2: '',
                direction: true,
                threshold: 50,
                granular: true,
                model_options: [
                    { text:'FinMultiQA', value:'finmultiqa' },
                    { text:'Finbert', value:'finbert' },
                    { text:'MultiQA', value:'multiqa' },
                    { text:'MSMarco', value:'msmarco' },
                    ],
                model: 'finmultiqa'
            },
            results: {
                granular: true, 
                queries: {}
            },
            display: {
                loading: false, 
                headers: [
                    { text: 'Entity 1', align: 'left', value: 'closest_relation.e1', width:'10%' },
                    { text: 'Entity 2', value: 'closest_relation.e2', width:'10%' },
                    { text: 'Relation', value: 'closest_relation.relation', align: 'center', width:'6%' },
                    { text: 'Relation Score', value: 'relation_score', align: 'center', width:'6%' },
                    { text: 'Abstract', value: 'sentences', width:'43%' },
                    { text: 'Title', value: 'title', width: '15%' },
                    { text: 'Date', value: 'date', width: '10%' },
                ],
                sort_by: 'relation_score',
                sort_desc: true
            },
            relation_labels: {
                all: {
                    coarse: [ 'DIRECT', 'INDIRECT' ],
                    granular: [  'ATTRIBUTE', 'FUNCTION', 'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'NONE', 'CONDITION', 'COMPARISON', 'UNCERTAIN' ]
                },
                selected: []
            }
        }
    },
    props: {
        msg: String
    },
    methods: {
        // FORM
        submit(event) {
            this.display.loading = true
            event.preventDefault()
            const path = 'http://137.132.83.244/finsearchBackend/query'
            const query_threshold = this.form.threshold / 100;
            const search_query = {
                entity1: this.form.entity1,
                entity2: this.form.entity2,
                direction: this.form.direction,
                threshold: query_threshold,
                granular: this.form.granular,
                model: this.form.model
            }
            axios.post(path, search_query).then(response => {
                this.results.queries = response.data.results
                this.results.granular = response.data.granular
                if (this.results.granular) {
                    this.relation_labels.selected = this.relation_labels.all.granular
                } else {
                    this.relation_labels.selected = this.relation_labels.all.coarse
                }
                this.display.loading = false 
            }).catch((error) => {
                console.error(error)
            })
        },
        directionToggle() {
            if (this.form.direction) {
                return "Ordered"
            } else {
                return "Unordered"
            }
        },
        granularToggle() {
            if (this.form.granular) {
                return "Granular Relations"
            } else {
                return "Coarse Relations"
            }
        },
        // DISPLAY TABLE
        displayRelationScore(score) {
            return (score * 100).toFixed(0)
        },
        displayAbstract(sentences, closest_relation) {
            let e1_start = closest_relation.e1_start
            let e1_end = closest_relation.e1_end
            let e2_start = closest_relation.e2_start
            let e2_end = closest_relation.e2_end
            let entity1 = "<span class='entity entity1' style='border-radius:5px; padding:5px;'>" + closest_relation.e1 + "</span>"
            let entity2 = "<span class='entity entity2' style='border-radius:5px; padding:5px;'>" + closest_relation.e2 + "</span>"

            if (e1_start < e2_start) {
                let before = sentences.slice(0, e1_start).join(" ")
                let between = sentences.slice(e1_end+1, e2_start).join(" ")
                let after = sentences.slice(e2_end+1).join(" ")
                return "<p class='abstract'>" + [before, entity1, between, entity2, after].join(" ") + "</p>"
            } else {
                let before = sentences.slice(0, e2_start).join(" ")
                let between = sentences.slice(e2_end+1, e1_start).join(" ")
                let after = sentences.slice(e1_end+1).join(" ")
                return "<p class='abstract'>" + [before, entity2, between, entity1, after].join(" ") + "</p>"
            }
            
        },
        // FILTERING
        relationFilterOptions() {
            if (this.results.granular) {
                return this.relation_labels.all.granular
            } else {
                return this.relation_labels.all.coarse
            }
        },
        relationFilter() {
            return Object.values(this.results.queries).filter(row => {
                return this.relation_labels.selected.includes(row.closest_relation.relation)
            })
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

.entity {
    border-radius: 5px;
    padding: 4px;
    line-height: 1.8;
    font-weight: bold;
}

.entity1 {
    background-color:#0331A1;
    color: white;
}

.entity2 {
    background-color:#F88810;
    color: white;
}

.abstract {
    padding-top: 7px;
    margin-top: 0px; 
    margin-bottom: 0px;
    line-height: 1.8;
}
</style>
