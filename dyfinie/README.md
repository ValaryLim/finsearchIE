# DyFinIE: Financial Extraction
This directory contains information on how we train DyFinIE, generate predictions for DyFinIE and baselines, and evaluate the results.

## Table of Contents
- [Directory Structure](#directory-structure)
- [DyFinIE](#dyfinie)
    - [DyFinIE Training](#dyfinie-training)
    - [DyFinIE Prediction](#dyfinie-prediction)
- [Baselines](#baselines)
    - [OpenIE]#openie)
    - [SRL](#srl)
- [Evaluation](#evaluation)

## Directory Structure

    .
    ├── dygiepp                     # Information on Training and Predicting with DyFinIE    
    ├── baselines                   # Information on Predicting with Baseline Models
    │   ├── openie                      # OpenIE Predictions
    │   └── srl                         # SRL Predictions
    ├── evaluation                  # Evaluation scripts
    │   ├── insert eval scripts here
    │   └── insert eval scripts here
    └── finmechanic                 # Dataset Used to Train DyFinIE

## DyFinIE Training (Dygiepp)
We provide scripts and configurations to train DyFinIE in [finsearchIE/dyfinie/dygiepp/](https://github.com/ValaryLim/finsearchIE/tree/main/dyfinie/dygiepp/).

### Getting Started
1. Clone the [Dygiepp repository](https://github.com/dwadden/dygiepp)
2. Follow the instructions in [Dygiepp](https://github.com/dwadden/dygiepp) to install required dependencies
3. Copy files in the [finsearchIE/dyfinie/dygiepp/](https://github.com/ValaryLim/finsearchIE/tree/main/dyfinie/dygiepp/) directory into Dygiepp

### Model Training
Navigate to your local Dygiepp root repository.

To prepare the dataset for model training:
```
bash scripts/data/get_finance.sh 
```

To train DyGIE++ model:
```
python scripts/tuning/(model).py --data_dir (path/to/data/) --serial_dir (path/to/model/)
```

To evaluate trained DyGIE++ model: 
```
allennlp evaluate \ 
(path/to/model) \ 
(path/to/test.json) \ 
--include-package dygie 
```

### Model Prediction
```
allennlp predict \ 
(path/to/model/) \ 
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
- `ie_evaluation.py`: Evaluates performance of information extraction models
- `ner_model_performance.py`: Code to compare DyFinIE with off-the-shelf NER models
- `validation_curve_plots.py`: Code to plot validation curves of DyFinIE tuning 