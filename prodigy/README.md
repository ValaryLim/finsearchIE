# Prodigy
We make use of [Prodigy](https://prodi.gy/) to annotate our FinMechanic dataset. This directory provides instructions on loading the sample data onto Prodigy, processing annotated data, and processing prediction data into a format accepted by Prodigy. 

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the [Python Installation Guide](https://www.python.org/downloads/) for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n prodigy_annotation python=3.9
```

This project will also require the paid [Prodigy](https://prodi.gy/) software. For instructions on how to install Prodigy, please proceed to [their website](https://prodi.gy/buy).

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Set-up Prodigy according to instructions available on [https://prodi.gy/](https://prodi.gy/).
3. Move into the Prodigy directory
    ```sh
    cd finsearchIE/prodigy/
    ```
4. Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

## Loading Data for Relation Annotation
To load data onto Prodigy for relation extraction (based on our relation schema), run the following command:
```sh
prodigy rel.manual (dataset_name) en_core_web_sm (path_to_dataset.json) --label ATTRIBUTE,FUNCTION,POSITIVE,NEGATIVE,NEUTRAL,NONE,UNCERTAIN,CONDITION,BETTER,COREFERENCE --span-label ENTITY --add-ents --wrap
```

For example, to annotate FinMechanic, we perform the following steps:
1. Move into FinSearchIE directory
    ```sh
    cd finsearchIE/
    ```
2. Load FinMechanic data into Prodigy and start Prodigy session
    ```sh
    prodigy rel.manual finmechanic en_core_web_sm financial_corpus/data/abstracts/sample_abstracts.json --label ATTRIBUTE,FUNCTION,POSITIVE,NEGATIVE,NEUTRAL,NONE,UNCERTAIN,CONDITION,BETTER,COREFERENCE --span-label ENTITY --add-ents --wrap
    ```

## Downloading Annotated Data
To export datasets from Prodigy, run:
```sh 
prodigy db-out (dataset_name) > (path_to_output.jsonl)
```

For example, to download the FinMechanic dataset, we perform the following steps:
1. Move into FinSearchIE directory
    ```sh
    cd finsearchIE/
    ```
2. Load FinMechanic data into Prodigy and start Prodigy session
    ```sh
    prodigy db-out finmechanic > prodigy/data/finmechanic_raw.jsonl
    ```

## Processing Downloaded Data
We provide a Python script, [prodigy_processing.py](prodigy_processing.py), to format annotated data downloaded from Prodigy into a format suitable for training DyGIE++ models. To run the script:

1. Move into Prodigy directory
    ```sh
    cd finsearchIE/
    ```
2. Call [prodigy_processing.py](prodigy_processing.py) script
    ```sh
    python prodigy/prodigy_processing.py (downloaded_prodigy_file.jsonl) (processed_file_path)
    ```
    For example, for FinMechanic, we run:
    ```sh
    python prodigy/prodigy_processing.py prodigy/data/finmechanic_raw.jsonl prodigy/data/finmechanic_processed.jsonl
    ```

## Loading Annotated/Predicted Relation Data
To load existing annotated data from the Prodigy database, run:
```sh
prodigy rel.manual (new_dataset_name) en_core_web_sm dataset:(dataset_name) --label ATTRIBUTE,FUNCTION,POSITIVE,NEGATIVE,NEUTRAL,NONE,UNCERTAIN,CONDITION,BETTER,COREFERENCE --span-label ENTITY --add-ents --wrap
```

To load predictions from DyFinIE into Prodigy:
1. Move into Prodigy directory
    ```sh
    cd finsearchIE/
    ```
2. Call [prodigy_formatting.py](prodigy_formatting.py) script
    ```sh
    python prodigy/prodigy_formatting.py (prediction_file.json) (formatted_prediction_file.jsonl)
    ```
3. Load formatted file into Prodigy
    ```sh
    cat (formatted_prediction_file.jsonl) | prodigy rel.manual (dataset_name) en_core_web_sm - --loader jsonl --label ATTRIBUTE,FUNCTION,POSITIVE,NEGATIVE,NEUTRAL,NONE,UNCERTAIN,CONDITION,BETTER,COREFERENCE,DIRECT,INDIRECT --span-label ENTITY --add-ents --wrap
    ```

## Built With
* [Python](https://www.python.org/)
* [Prodigy](https://prodi.gy/)