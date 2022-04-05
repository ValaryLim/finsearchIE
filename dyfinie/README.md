# DyFinIE
## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n finsearch_backend_querier python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
pip install -r requirements.txt
```

## Baselines
We provide scripts to generate predictions for baseline models OpenIE, SRL, and ReLogic (Deprecated) in [financeOpenIE/dyfinie/baselines/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/baselines/). 

To run the baseline models:
1. Move into [financeOpenIE/dyfinie/baselines/](https://github.com/ValaryLim/financeOpenIE/tree/main/dyfinie/baselines/) directory
2. `pip install -r (model)_requirements.txt`
3. `python (model)_prediction.py`

## Others
