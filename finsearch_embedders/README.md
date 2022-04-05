# FinSearch Embedders
## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/finsearchIE/tree/main/finsearch_backend_query/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```

## Run Training Scripts
```
python (model)_training.py
```

## Run Evaluation 
```
python evaluate_encoder.py
```