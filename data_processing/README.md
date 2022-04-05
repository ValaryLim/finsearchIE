# Data Processing Files
## Folder Structure
    .
    ├── article_processing.py       # Pipeline to process and combine financial abstracts
    ├── external_processing.py      # Pipeline to process external dataset           
    ├── prodigy_processing.py       # Pipeline to convert Prodigy output into DyFinIE input
    └── prodigy_unprocessing.py     # Pipeline to convert DyFinIE output into Prodigy input

## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```

## Running Python Scripts
To run the scrapers, call `python (filename)`.
