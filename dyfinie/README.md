# DyFinIE
## DyFinIE Training (Dygiepp)
We provide scripts and configurations to train DyFinIE in [financeOpenIE/dyfinie/dygiepp/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/dygiepp/).

### Getting Started
1. Clone the [Dygiepp repository](https://github.com/dwadden/dygiepp)
2. Follow the instructions in [Dygiepp](https://github.com/dwadden/dygiepp) to install required dependencies
3. Copy files in the [financeOpenIE/dyfinie/dygiepp/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/dygiepp/) directory into Dygiepp

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
We provide scripts to generate predictions for baseline models OpenIE, SRL, and ReLogic (Deprecated) in [financeOpenIE/dyfinie/baselines/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/baselines/). 

To run the baseline models:
1. Move into [financeOpenIE/dyfinie/baselines/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/baselines/) directory
2. `pip install -r (model)_requirements.txt`
3. `python (model)_prediction.py`

## Evaluation
