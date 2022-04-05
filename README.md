# Searchable Financial Knowledge Base

## Folder Structure
    .
    ├── ...
    ├── data_processing                 # Scripts to Process Data              
    ├── dyfinie                         # DyFinIE model implementation
    │   ├── baselines                       # Baseline model prediction pipelines
    │   ├── analyst_model               # Documentation files for Analyst Recommendation Model set-up
    |   ├── data                        # Local data for project
    |   ├── dags                        # Dag files
    |   │   ├── analyst_model           # Dag files for Analyst Recommendation Model
    |   |   ├── setup_tests             # Dag files to test project set-up
    |   |   └── fx_rates.py 
    |   ├── gcp                         # Documentation files for Google Cloud Platform set-up
    |   ├── scrapers                    # Contains scrapers for retrieving financial abstracts
    │   └── requirements.txt
    ├── finsearch_frontend              # FinSearch Frontend Application
    ├── finsearch_backend_query         # FinSearch Backend Querier Microservice Application
    │   └── apache                          # Instructions to run Querier on Apache
    ├── finsearch_backend_embedder      # FinSearch Backend Embedder Microservice Application
    ├── scrapers                        # Financial abstract scrapers
    └── ...
