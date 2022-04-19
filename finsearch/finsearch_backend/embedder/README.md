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
    ├── embedding_models                    # Files to Train and Evaluate Embedder Models
    │   ├── finsemantic                         # FinSemantic Dataset
    |   ├── evaluate_encoder.py                 # Script to Evaluate Encoder
    |   ├── finmsmarco_training.py              # Script to Train FinMsMarcoQA
    │   └── finmultiqa_training.py              # Script to Train FinMultiQA
    ├── finsearch_embedder                  # Embedder Flask Application
    ├── finkb_embeddings_generation.py      # Script to Generate Embeddings from FinKB
    ├── knn_graph_generation.py             # Script to Generate Graphs from Embeddings
    └── requirements.txt                    # Requirements

## Data Preparation
### Train Embedder Models
We train two custom Embedder models, one of which `finmultiqa`, has been selected and integrated into our Embedder application. We provide the scripts in the `embedding_models/` directory.
- To train FinMultiQA:
    ```sh
    python finmultiqa_training.py
    ```
- To train FinMsMarcoQA:
    ```sh
    python finmsmarco_training.py
    ```
Both these models will be automatically saved within the `finsearch_embedder/models/` directory.

We also provide `evaluate_encoder.py`, the script used to evaluate all Encoder models. To run the script:
1. Modify `evaluate_encoder.py` to include the list of Encoders you wish to compare
2. Ensure you are in the `embedding_models/` directory
    ```sh
    cd finsearchIE/finsearch/finsearch_backend/embedder/embedding_models/
    ```
3. Run the script
    ```sh
    python evaluate_encoder.py
    ```

### Generate FinKB Embeddings
The `finkb_embeddings_generation.py` script generates embeddings for all models. To run the script:
1. Transfer the `finance_coarse_coref.jsonl` and `finance_granular_coref.jsonl` relational triplet prediction files into the `finsearch_embedder/data/finkb/` directory.
2. Run the script
    ```sh
    python finkb_embeddings_generation.py
    ```

### Generate KNN Graphs from FinKB Embeddings
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