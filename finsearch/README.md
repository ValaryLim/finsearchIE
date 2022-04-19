# FinSearch
FinSearch is a service that allows users to query for relevant abstracts from our financial knowledge base, FinKB. Users enter 2 keywords or phrases, and the service trawls through its corpus of almost 1,000,000 relational triplets and aggregates them to return the most relevant results. The service has a separate frontend and backend system, with the backend consisting of two separate microservices, a Querier, and an Embedder.

## Table of Contents
- [FinSearch Frontend](#finsearch-frontend)
- [FinSearch Backend](#finsearch-backend)
    - [Querier Microservice](#querier-microservice)
    - [Embedder Microservice](#embedder-microservice)
- [Directory Structure](#directory-structure)

## FinSearch Frontend
The [FinSearch Frontend](finsearch_frontend/) is a responsive and aesthetically pleasing user interface that users can interact with to fetch data from our system. The application is intuitive and allows users to easily identify what parameters the service can accept and tweak. It is deployed using [surge](https://surge.sh/) at [http://finsearch.surge.sh/](http://finsearch.surge.sh).

The Frontend makes use of calls Rest API endpoints exposed by the [Backend Querier Microservice](#querier-microservice) to retrieve data from our Backend, and renders it in the form of a sortable table.

![](media/finsearch-frontend.gif)

We provide more details of how to run the application in the [FinSearch Frontend Directory](finsearch_frontend/).

## FinSearch Backend
![](media/finsearch-backend-architecture.png)

### Querier Microservice
The [Querier microservice](finsearch_backend/querier/) exposes REST API endpoints for the Frontend service to access data, and is served using Apache. The querier service parses the API requests received, and generates the queries in a format that can be used by our [Embedder Microservice](#embedder-microservice).

### Embedder Microservice
The [Embedder microservice](finsearch_backend/embedder/) can only be queried via the [Querier Microservice](#querier-microservice), and is kept perpetually running on a local machine. It is completely inaccessible by external sources. This microservice is responsible for pre-loading the embedding models and data into the system memory, receiving the formulated queries from the Querier service, and trawling through the database to return the most applicable abstracts in a JSON format.

As our embedding models and data are memory-intensive, the Embedder takes a significant time to cold start. We have separated the Querier and Embedder microservice to allow for the creation of a custom Python environment (required for some embedding models), and to reduce the need to reload our embedding models and data to keep our service highly performant.

## Directory Structure

    .
    ├── finsearch_frontend    
    ├── finsearch_backend
    │   ├── querier
    |   ├── embedder
    │   └── embedding models
    └── media
