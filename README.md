# Searchable Financial Knowledge Base

## Folder Structure
    .
    ├── ...
    ├── scrapers                        # Local airflow directory
    │   ├── dags                        # 
    |   │   └── dag_bags.py     
    │   ├── airflow-webserver.pid 
    │   ├── airflow.cfg                 # Airflow configuration file
    │   ├── airflow.db 
    │   └── webserver_config.py                
    ├── SGXDataWarehouse                # Github Project
    │   ├── airflow                     # Documentation files for local airflow configuration
    │   ├── analyst_model               # Documentation files for Analyst Recommendation Model set-up
    |   ├── data                        # Local data for project
    |   ├── dags                        # Dag files
    |   │   ├── analyst_model           # Dag files for Analyst Recommendation Model
    |   |   ├── setup_tests             # Dag files to test project set-up
    |   |   └── fx_rates.py 
    |   ├── gcp                         # Documentation files for Google Cloud Platform set-up
    |   ├── scrapers                    # Contains scrapers for retrieving financial abstracts
    │   └── requirements.txt
    ├── scrapers                        # Local airflow directory
    └── ...
