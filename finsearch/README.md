# FinSearch
## Description 
FinSearch is a service that allows users to query for relevant abstracts from our financial knowledge base, FinKB. Users enter 2 keywords or phrases, and the service trawls through its corpus of almost 1,000,000 relational triplets and aggregates them to return the most relevant results. The service has a separate frontend and backend system, with the backend consisting of two separate microservices, a Querier, and an Embedder.

## [FinSearch Frontend](finsearch_frontend/)


## Table of Contents
- [Folder Structure](#folder-structure)
- [Installation and Usage](#installation-and-usage)
- [Contributors](#contributors)
- [Guides and Resources](#guides-and-resources)
- [License](#license)

## Folder Structure
This directory is split into 3 components
    .
    ├── ...
    ├── data_processing                 # Scripts to process data           
    ├── datasets                        # FinMechanic and FinSemantic Data    
    │   ├── finmechanic                     # Raw dataset for DyFinIE model training
    │   └── finsemantic                     # Raw dataset for FinMultiQA model training
    ├── dyfinie                         # DyFinIE model implementation
    │   ├── baselines                       # Baseline model prediction pipelines
    │   ├── dygiepp                         # Files to Run DyFinIE Tuning and Prediction
    |   └── evaluation                      # Evaluation scripts for DyFinIE
    ├── finkb                           # FinKB generation
    |   └── evaluation                      # Evaluation scripts for FinKB
    ├── finsearch_frontend              # FinSearch Frontend Application
    ├── finsearch_backend_query         # FinSearch Backend Querier Microservice Application
    │   └── apache                          # Instructions to run Querier on Apache
    ├── finsearch_backend_embedder      # FinSearch Backend Embedder Microservice Application
    ├── finsearch_embedders             # Scripts to train financial multiqa and msmarco models
    ├── scrapers                        # Financial abstract scrapers
    ├── utils                           # Utilities folder for scripts
    └── ...

## Installation and Usage

## Contributors

## Guides and Resources

## License
**MIT License**

Copyright (c) 2021-2022 Valary Lim Wan Qian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.