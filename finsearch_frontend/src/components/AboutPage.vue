<template>
  <v-container fluid>
    <v-layout row wrap>
      <v-flex xs12 class="text-xs-center" mt-5>
        <h2>About</h2>
        <p class="text-left">
            <span class="name">FinSearch</span> is a service that allows users to query for relevant abstracts 
            from a financial knowledge rebase, <span class="name">FinKB</span>. 
            The service accepts two entities and returns a table of abstracts with entity-relations involving 
            entities similar to that queried. 
            The service has both a frontend and backend system, with the backend consisting of two 
            separate microservices, a querier and an embedder.
        </p>
        <p class="text-left">
            For more information on the development of <span class="name">FinKB</span> and 
            <span class="name">FinSearch</span>, please refer to our 
            <a href="https://github.com/ValaryLim/financeOpenIE">Paper</a> and 
            <a href="https://github.com/ValaryLim/financeOpenIE">Github Repository</a>.
        </p>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  //name: "Landing"
};
</script>

<style scoped>
.name {
    font-weight: 600;
}
</style>