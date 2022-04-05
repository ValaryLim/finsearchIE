# FinKB Generation and Evaluation
## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/financeOpenIE/tree/main/finsearch_backend_query/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```

## Generate FinKB
This step calls the prediction model on the full financial corpus to generate FinKB.
```
python generate_finkb.py
```

## Generate Encoded FinKB
This step calls the specified encoder models on all relational triplets in FinKB and saves it into a file for use in FinSearch.
```
python generate_encoded_finkb.py
```

## Run Evaluation 
Evaluation function to compare performance of different embedding models.
```
python evaluate_encoder.py
```