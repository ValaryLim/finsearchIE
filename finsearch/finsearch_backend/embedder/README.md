# FinSearch Backend Embedder Microservice
The Embedder microservice is responsible for pre-loading the embedding models and data into the system memory, receiving the formulated queries from the Querier service, and trawling through the database to return the most applicable abstracts in a JSON format. It should be kept perpetually running on the machine, and is only access by the Querier microservice.

## How the Embedder Works
On receiving a query, the Embedder Microservice:
1. Embeds both search entities using the selected embedding model
2. Utilises a modified [Approximate Nearest Neighbour Descent search algorithm](https://pynndescent.readthedocs.io/en/latest/) to retrieve an approximation of the most semantically similar relational triplets.
3. Aggregates the top relations by abstract and assigns a similarity score to the abstract
4. Sorts the abstracts and filters for the top 1000 by abstract similarity score
5. Returns the top 1000 abstracts as a json

We have provided more details in our paper.

## Directory Structure

    .
    ├── finsearch_embedder    
    ├── embedding_models
    │   ├── querier
    |   ├── embedder
    │   └── embedding models
    └── data_preparation.py

## Data Preparation
The Embedder microservice requires 3 main pre-processing steps to function, (1) generating embeddings of the relational triplets in FinKB, (2) generating a k-nearest neighbours graph required for Approximate Nearest Neighbour Descent Search, and (3) integrating data into Embedder application. We provide details on the required steps below.

### Generate Model Embeddings

### 
The Embedder Microservice requries a data preparation step to generate the k-nearest neighbours graph required for Approximate Nearest Neighbour Descent. To create the k-nearest neighbour graph:
1. Ensure that the .jsonl files containing relational triplet embeddings produced in Step 1 are in `finsearchIE/finsearch/finsearch_backend/embedder/finsearch_embedder/data/(model_name)/` directory, where `model_name` is the name of the Embedder model, e.g. `ProsusAI/finbert` for FinBERT.
2. Call the [knn_graph_generation.py script](knn_graph_generation.py)
    ```sh
    python knn_graph_generation.py '(model_name)'
    ```
    For example, `python knn_graph_generation.py 'ProsusAI/finbert'`

### Integrating Data into Embedder Application
The Embedder application hardcodes the directories of data required. If you wish to add more models or data, you will need to modify the `models`, `relation_info`, `relation_train` paths included in [app.py](finsearch_embedder/app.py).

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the [Python Installation Guide](https://www.python.org/downloads/) for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n finsearch_backend_embedder python=3.9
```

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the FinSearch Backend Querier Microservice directory
    ```sh
    cd finsearchIE/finsearch/finsearch_backend/embedder/
    ```
3. Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To start the project:
1. Move into the FinSearch Backend Embedder Microservice directory
    ```sh
    cd finsearchIE/finsearch/finsearch_backend/embedder/
    ```
2. Run application
    ```sh
    python app.py
    ```

## Built With
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)