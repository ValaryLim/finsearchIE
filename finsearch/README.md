# FinSearch
FinSearch is a service that allows users to query for relevant abstracts from our financial knowledge base, FinKB. Users enter 2 keywords or phrases, and the service trawls through its corpus of almost 1,000,000 relational triplets and aggregates them to return the most relevant results. The service has a separate frontend and backend system, with the backend consisting of two separate microservices, a Querier, and an Embedder.

## Table of Contents
- [FinSearch Frontend](#finsearch-frontend)
- [FinSearch Backend](#finsearch-backend)
    - [Querier Microservice](#querier-microservice)
    - [Embedder Microservice](#embedder-microservice)
- [Installation and Usage](#installation-and-usage)
- [Contributors](#contributors)
- [Guides and Resources](#guides-and-resources)
- [License](#license)

## FinSearch Frontend
The [FinSearch Frontend](finsearch_frontend/) is a responsive and aesthetically pleasing user interface that users can interact with to fetch data from our system. The application is intuitive and allows users to easily identify what parameters the service can accept and tweak. It is deployed using [surge](https://surge.sh/) at [http://finsearch.surge.sh/](http://finsearch.surge.sh).

The Frontend makes use of calls Rest API endpoints exposed by the [Backend Querier Microservice](#querier-microservice) to retrieve data from our Backend, and renders it in the form of a sortable table.

![](media/finsearch-frontend.gif)

We provide more details of how to run the application in the [FinSearch Frontend Directory](finsearch_frontend/).

## FinSearch Backend

### Querier Microservice

### Embedder Microservice




## Folder Structure
This directory is split into 3 components
    .
    ├── ...
    ├── data_processing                 # Scripts to process data           
    ├── datasets                        # FinMechanic and FinSemantic Data    
    │   ├── finmechanic                     # Raw dataset for DyFinIE model training
    │   └── finsemantic                     # Raw dataset for FinMultiQA model training
    ├── dyfinie                         # DyFinIE model implementation
    │   ├── baselines                       # Baseline model prediction pipelines
    │   ├── dygiepp                         # Files to Run DyFinIE Tuning and Prediction
    |   └── evaluation                      # Evaluation scripts for DyFinIE
    ├── finkb                           # FinKB generation
    |   └── evaluation                      # Evaluation scripts for FinKB
    ├── finsearch_frontend              # FinSearch Frontend Application
    ├── finsearch_backend_query         # FinSearch Backend Querier Microservice Application
    │   └── apache                          # Instructions to run Querier on Apache
    ├── finsearch_backend_embedder      # FinSearch Backend Embedder Microservice Application
    ├── finsearch_embedders             # Scripts to train financial multiqa and msmarco models
    ├── scrapers                        # Financial abstract scrapers
    ├── utils                           # Utilities folder for scripts
    └── ...

## Installation and Usage


## Guides and Resources
