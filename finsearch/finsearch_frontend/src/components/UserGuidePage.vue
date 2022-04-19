<template>
    <v-container fluid>
        <v-layout row wrap>
            <v-flex xs12 class="text-xs-center" mt-5>
                <h2>User Guide</h2>
            </v-flex>
            <v-flex xs12 class="text-left" mt-5>
                <h4>Form Options</h4>
            </v-flex>
            <v-simple-table>
                <template v-slot:default>
                <thead>
                    <tr>
                        <th class="text-left">Option</th>
                        <th class="text-left">Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-left">Entity 1 / Entity 2</td>
                        <td class="text-left">
                            <span class="variable">Entity 1</span>: First search entity
                            <br>
                            <span class="variable">Entity 2</span>: Second search entity
                            <br>
                            <hr>
                            Entity 1 and Entity 2 refer to the entities you're interested in searching for.
                            <br>
                            For instance, if you wish to search about how 
                            '<span class="fw-bold">economic growth</span>' can affect
                            '<span class="fw-bold">interest rates</span>', 
                            type '<span class="fw-bold">economic growth</span>' in the search box for Entity 1 
                            and '<span class="fw-bold">interest rates</span>' in the search box for Entity 2.
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left">Threshold Selection</td>
                        <td class="text-left">
                            <span class="variable">Threshold</span>: Integer value representing minimum relation score
                            <br>
                            <hr>
                            Each article in our database is given a relation score based on its similarity
                            with the two search entities. Threshold selects the minimum relation score
                            required for articles to be returned.
                            For example, a threshold of 50 will return only abstracts with a relation score 
                            greater than 50.
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left">Direction Toggle</td>
                        <td class="text-left">
                            <span class="variable">Ordered</span>: Entity 1 and Entity 2 will strictly be 
                            compared with the first and second entity respectively of all relations in our 
                            database
                            <br>
                            <span class="variable">Unordered</span>: Entity 1 and Entity 2 will be compared 
                            with both the first and second entity of all relations in our database
                            <br>
                            <hr>
                            Some relations in our database have a causal relation, where Entity 1 affects 
                            Entity 2. 
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left">Relation Granularity Toggle</td>
                        <td class="text-left">
                            <span class="variable">Granular</span>: Retrieve granular relations
                            <br>
                            <span class="variable">Coarse</span>: Retrieve coarse relations
                            <br>
                            <hr>
                            Our financial knowledge base consists of both a coarse and granular relation set. 
                            Refer to the Relation Table below for more details on each relation set. 
                        </td>
                    </tr>
                    <tr>
                        <td class="text-left">Model Selection</td>
                        <td class="text-left">
                            <span class="variable">FinMultiQA</span>: Custom MultiQA model trained on financial data
                            <br>
                            <span class="variable">Finbert</span>: Bert embedder trained on financial data (ProsusAI/finBERT)
                            <br>
                            <span class="variable">MultiQA</span>: Bert embedder trained on question-answer datasets (alontalmor/MultiQA)
                            <br>
                            <span class="variable">MsMarco</span>: Embedder trained on question-answer datasets for page ranks (cross-encoder/ms-marco-MiniLM-L-12-v2)
                            <br>
                            <hr>
                            We compute similarity of two entities by taking the cosine similarity of the 
                            embeddings generated by our search model. 
                        </td>
                    </tr>
                </tbody>
                </template>
            </v-simple-table>
            <v-flex xs12 class="text-left" mt-5>
                <p></p>
                <h4>Relation Table</h4>
            </v-flex>
            <v-simple-table>
                <template v-slot:default>
                <thead>
                    <tr>
                        <th class="text-left">Coarse Classification</th>
                        <th class="text-left">Granular Classification</th>
                        <th class="text-left">Definition</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="text-left">Direct</td>
                        <td class="text-left">Attribute</td>
                        <td class="text-left">Entity 1 is an attribute/subset of Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Direct</td>
                        <td class="text-left">Function</td>
                        <td class="text-left">Entity 1 is used for/a model of Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Positive</td>
                        <td class="text-left">Entity 1 positively affects/correlates with Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Negative</td>
                        <td class="text-left">Entity 1 negatively affects/correlates with Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Neutral</td>
                        <td class="text-left">Entity 1 affects/correlates with Entity 2 (no direction specified)</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">None</td>
                        <td class="text-left">Entity 1 does not affect/has no relation with Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Condition</td>
                        <td class="text-left">If Entity 1, then Entity 2. Entity 2 occurs in the event of Entity 1</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Comparison</td>
                        <td class="text-left">Entity 1 is better than/different from Entity 2</td>
                    </tr>
                    <tr>
                        <td class="text-left">Indirect</td>
                        <td class="text-left">Uncertain</td>
                        <td class="text-left">Relationship between Entity 1 and Entity 2 is uncertain</td>
                    </tr>
                </tbody>
                <br>
                <br>
                </template>
            </v-simple-table>
        </v-layout>
    </v-container>
</template>

<script>
export default {
  //name: "Landing"
};
</script>

<style>
hr {
    height: 1px;
    border-width: 1px;
    padding: 0;
    margin: 5px;
}

.variable {
    font-family: 'Roboto Mono', monospace;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #0331A1;
    font-weight: 500;
}
</style>