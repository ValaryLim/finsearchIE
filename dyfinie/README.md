# DyFinIE: Financial Extraction
This directory contains information on how we train DyFinIE, generate predictions for DyFinIE and baselines, and evaluate the results.

## Table of Contents
- [Directory Structure](#directory-structure)
- [DyFinIE](#dyfinie)
    - [Model Training](#model-training)
    - [Model Evaluation](#model-evaluation)
    - [Model Prediction](#model-prediction)
- [Baselines](#baselines)
    - [OpenIE](#openie)
    - [SRL](#srl)
- [Evaluation](#evaluation)
    - [Information Extraction Evaluation](#information-extraction-evaluation)

## Directory Structure

    .
    ├── dygiepp                     # Information on Training and Predicting with DyFinIE    
    ├── baselines                   # Information on Predicting with Baseline Models
    │   ├── openie                      # OpenIE Predictions
    │   └── srl                         # SRL Predictions
    ├── evaluation                  # Evaluation scripts
    │   ├── ie_evaluation.py            # DyFinIE Compared to OpenIE Baselines
    │   └── ner_evaluation.py           # DyFinIE Compared to NER Models
    └── finmechanic                 # Dataset Used to Train DyFinIE

## DyFinIE
### Installation
1. Clone the [DyGIE++ Repository](https://github.com/dwadden/dygiepp)
   ```sh
   git clone https://github.com/dwadden/dygiepp.git
   ```
2. Navigate into DyGIE++ Repository and Install Packages
    ```sh
    conda create --name dygiepp python=3.7
    pip install -r requirements.txt
    conda develop .   # Adds DyGIE to your PYTHONPATH
    ```
3. Copy files in [finsearchIE/dyfinie/dygiepp/](finserachIE/dyfinie/dygiepp/) into DyGIE++ directory
    ```sh
    cp finsearchIE/dyfinie/dygiepp/hyperparam_config/finance.json dygiepp/hyperparam_config/finance.json
    cp -r finsearchIE/dyfinie/dygiepp/scripts/ dygiepp/scripts/
    ```
4. Copy FinMechanic Dataset into DyGIE++ directory
    ```sh
    cp -r finsearchIE/dyfinie/finmechanic/ dygiepp/
    ```

### Model Training
1. Navigate to DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
2. Copy FinMechanic Coarse Relaton data into `data/dyfinie_coarse/processed_data/` and Granular Relation data into `data/dyfinie_granular/processed_data/`
    ```sh
    # coarse data
    mkdir data/dyfinie_coarse/processed_data/
    cp -r finmechanic/coarse/ data/dyfinie_coarse/processed_data/

    # granular data
    mkdir data/dyfinie_granular/processed_data/
    cp -r finmechanic/granular/ data/dyfinie_granular/processed_data/
    ```
3. Navigate into DyGIE++ Repository
    ```sh
    cd dygiepp
    ```
4. Prepare coarse and granular datasets
    ```sh
    bash preprocessing/dyfinie_coarse.sh
    bash preprocessing/dyfinie_granular.sh
    ``
5. Train DyGIE++ models
    ```sh
    python scripts/tuning/dyfinie_coarse.py --data_dir data/dyfinie_coarse/normalized_data/ --serial_dir model/dyfinie_coarse/

    python scripts/tuning/dyfinie_granular.py --data_dir data/dyfinie_granular/normalized_data/ --serial_dir model/dyfinie_granular/
    ```

### Model Evaluation
1. Navigate to DyGIE++ Repository
    ```sh
    cd dygiepp
    ```
2. Evaluate trained model
    ```sh
    # evaluate coarse performance
    allennlp evaluate \ 
    data/dyfinie_coarse/ \ 
    data/dyfinie_coarse/normalized_data/test.json \ 
    --include-package dygie 

    # evaluate granular performance
    allennlp evaluate \ 
    data/dyfinie_granular/ \ 
    data/dyfinie_granular/normalized_data/test.json \ 
    --include-package dygie 
    ```

### Model Prediction
1. Navigate to DyGIE++ Repository
    ```sh
    cd dygiepp
    ```
2. Process raw dataset
    ```sh
    python scripts/data/shared/normalize.py \
    (path_to_dataset)/processed_data/json \
    (path_to_dataset)/normalized_data/json \
    --file_extension=json \
    --max_tokens_per_doc=0 \
    --dataset=$config_name
    ```
3. Predict on normalized dataset
    ```sh
    allennlp predict \ 
    (path/to/model/) \  # example: model/dyfinie_coarse or model/dyfinie_granular
    (path/to/data/) \ 
    --predictor dygie \ 
    --include-package dygie \ 
    --use-dataset-reader \ 
    --output-file (output/to/pred.jsonl) \ 
    --silent 
    ```

## Baselines
We provide scripts to generate predictions for baseline models OpenIE and SRL in [finsearchIE/dyfinie/baselines/](finsearchIE/dyfinie/baselines/).

### OpenIE
#### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
3. Install Python packages
    ```sh
    pip install -r baselines/openie/requirements.txt
    ```

### Generate Predictions
To generate predictions for OpenIE:
1. Move into the DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
2. Call prediction script
    ```sh
    python baselines/openie/openie_prediction.py '(raw_file_path.json)' '(pred_data_path/)'
    ```
    For example, to predict on FinMechanic's Coarse Test dataset, we call:
    ```sh
    python baselines/openie/openie_prediction.py 'finmechanic/coarse/test.json' 'data/pred/openie'
    ```

### SRL
#### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
3. Install Python packages
    ```sh
    pip install -r baselines/srl/requirements.txt
    ```

### Generate Predictions
To generate predictions for OpenIE:
1. Move into the DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
2. Call prediction script
    ```sh
    python baselines/srl/srl_prediction.py '(raw_file_path.json)' '(pred_data_path/)'
    ```
    For example, to predict on FinMechanic's Coarse Test dataset, we call:
    ```sh
    python baselines/srl/srl_prediction.py 'finmechanic/coarse/test.json' 'data/pred/srl'
    ```


## Evaluation
### Initialisation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
3. Install Python packages
    ```sh
    pip install -r evaluation/requirements.txt
    ```

### Information Extraction Evaluation
We provide a [ie_evaluation.py](evaluation/ie_evaluation.py) script to evaluate the performance of the various Information Extraction models. To perform the evaluation:

1. Move into DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
2. Copy prediction files over into `data/predictions/(model)/(name)/(type).jsonl`
    - `model`: srl, openie or dyfinie
    - `name`: finmechanic/coarse or finmechanic/granular
    - `type`: train, dev, or test
3. Run evaluation script
    ```sh
    python evaluation/ie_evaluation.py
    ```

## Named Entity Recognition Evaluation
We provide a [ner_evaluation.py](evaluation/ner_evaluation.py) script to evaluate the performance of the various NER models compared to DyFinIE. To perform the evaluation:

1. Move into DyFinIE directory
    ```sh
    cd finsearchIE/dyfinie/
    ```
2. Copy DyFinIE test prediction over into `data/predictions/dyfinie/finmechanic/coarse/test.jsonl`
3. Run evaluation script
    ```sh
    python evaluation/ner_evaluation.py
    ```
