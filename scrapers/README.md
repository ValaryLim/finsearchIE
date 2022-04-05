# Financial Abstract Scrapers
This directory contains information on setting up and running the scrapers used to generate finacial abstracts in our database. 

## Getting Started
This project should be run on Python 3.7. A conda environment can be created using the following:
```bash
conda create -n financial_scrapers python=3.7
```

A [requirements.txt](https://github.com/ValaryLim/finsearchIE/tree/main/scrapers/requirements.txt) file is provided that contains the specifications of the packages used in the project. Run the following command to install the required packages.
```bash
conda activate financial_scrapers
pip install -r requirements.txt
```

## Run Scrapers
To run the scrapers, call `python (filename)`.