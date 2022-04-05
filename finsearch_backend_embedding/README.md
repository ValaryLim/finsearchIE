# FinSearch Backend Embedder Microservice
This service is responsible for loading the embedding models and data into the system memory, receiving the formulated queries, and trawling through the database to return the most applicable abstracts. This service is developed in Python on the Flask framework. 

## How It Works
On receiving a query, the Embedder Microservice:
1. Embeds both search entities using the selected embedding model
2. Utilises a modified [Approximate Nearest Neighbour Descent search algorithm][https://pynndescent.readthedocs.io/en/latest/] to retrieve an approximation of the most semantically similar relational triplets
3. Aggregates the top relations by abstract and assigns a similarity score to the abstract
4. Sorts the abstracts and filters for the top 1000 by abstract similarity score
5. Returns the top 1000 abstracts as a json

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