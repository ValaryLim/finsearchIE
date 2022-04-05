# Searchable Financial Knowledge Base
This repository contains code and instructions for the following processes:
1. Scraping financial abstracts
2. Data annotation using Prodigy 
3. Training and evaluating DyFinIE
4. FinKB generation adn evaluation
5. FinSearch service (FinSearch Frontend, Finsearch Backend Querier, FinSearch Backend Embedder)
6. Training and evaluating of FinMultiQA and FinMsMarco

Please refer to [Constructing a Searchable Knowledge Base from Financial Text using Information Extraction]() for more details.

FinSearch is hosted on [http://finsearch.surge.sh](http://finsearch.surge.sh).


## Folder Structure
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

## Built With
- Python 3.7
- Python Flask
- Vue.js

## Authors
Valary Lim Wan Qian - [Github](https://github.com/ValaryLim)