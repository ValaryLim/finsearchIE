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

A [requirements.txt](https://github.com/ValaryLim/finsearchIE/tree/main/dyfinie/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```
## Running Python Scripts
To run the scrapers, call `python (filename)`.

## Prodigy Annotation
### Start Labelling Session
To start labelling session, we run:
```
prodigy rel.manual (db_name) en_core_web_sm (filename) --label ATTRIBUTE,FUNCTION,POS,NEG,NEU,NONE,UNCERTAIN,CONDITION,BETTER,COREF --span-label ENTITY --add-ents --wrap 
```

### Reload Dataset
From Prodigy Database:
```
prodigy rel.manual (db_name) en_core_web_sm dataset:(db_name) --label ATTRIBUTE,FUNCTION,POS,NEG,NEU,NONE,UNCERTAIN,CONDITION,BETTER,COREF --span-label ENTITY --add-ents --wrap 
```

From Json File:
```
cat (path/to/input) | prodigy rel.manual (db_name) en_core_web_sm - --loader jsonl --label ATTRIBUTE,FUNCTION,POSITIVE,NEGATIVE,NEUTRAL,NONE,UNCERTAIN,CONDITION,COMPARISON,COREFERENCE,DIRECT,INDIRECT --span-label ENTITY --add-ents --wrap 
```


### Export Prodigy Datasets
After data annotation, we run the following line to export the dataset from Prodigy's database to a .jsonl file.
```
prodigy db-out (db_name) > (path/to/output.jsonl)
```
