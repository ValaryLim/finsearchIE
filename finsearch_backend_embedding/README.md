# FinSearch Backend Embedder Microservice
This service is responsible for loading the embedding models and data into the system memory, receiving the formulated queries, and trawling through the database to return the most applicable abstracts. This service is developed in Python on the Flask framework. 

## How It Works
On receiving a query, the Embedder Microservice:
1. Embeds both search entities using the selected embedding model
2. Utilises a modified [Approximate Nearest Neighbour Descent search algorithm](https://pynndescent.readthedocs.io/en/latest/) to retrieve an approximation of the most semantically similar relational triplets
3. Aggregates the top relations by abstract and assigns a similarity score to the abstract
4. Sorts the abstracts and filters for the top 1000 by abstract similarity score
5. Returns the top 1000 abstracts as a json

## Data Preparation
The Embedder Microservice requries a data preparation step to generate the k-nearest neighbours graph required for Approximate Nearest Neighbour Descent. Run the following steps to preprocess the graph:
1. Transfer .jsonl files containing embedded relational triplet predictions into finsearch_backend_embedding/data/(model_name)/ directory
2. Call [preprocessing.py script](https://github.com/ValaryLim/financeOpenIE/tree/main/finsearch_backend_embedding/preprocessing.py)
```bash
python preprocessing.py (model_name)
```
3. Modify paths for `models`, `relation_info`, `relation_train` in [app.py](https://github.com/ValaryLim/financeOpenIE/tree/main/finsearch_backend_embedding/app.py)

## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_embedder python=3.7
```

A [requirements.txt] file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```
## Usage
Run the following commands to enter the conda environment and start the application:
```bash
conda activate finsearch_backend_embedder
python app.py
```