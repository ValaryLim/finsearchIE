# Financial Abstract Corpus
This directory contains code used to retrieve and process financial abstracts to form the Financial Abstract corpus.

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the [Python Installation Guide](https://www.python.org/downloads/) for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n financial_corpus python=3.9
```

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the Financial Corpus directory
    ```sh
    cd finsearchIE/financial_corpus/
    ```
3. Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

## Financial Scrapers
Different scraping methods were used to retrieve relevant abstracts from different sources.

| Source | File | Scraping Method |
| --- | --- | --- |
| American Economic | `american_economic.py` | All abstracts from journals with 'Economic' or 'Accounting' in their name were retrieved. |
| American Accounting | `american_accounting.py` | All abstracts from journals with 'Economic' or 'Accounting' in their name were retrieved. |
| Wiley | `wiley.py` | All abstracts from journals tagged as 'Accounting' or 'Business & Management' were retrieved. |
| Oxford Academic | `oxford_academic.py` | All abstracts from journals with 'Economic' or 'Accounting' in their name were retrieved. |
| Springer | `springer.py` | Financial terms in [`keywords.txt`](scrapers/keywords.txt) were queried and all abstracts from search containing root word 'finance' (e.g. finance, financing, financial) were retrieved. |
| Elsevier | `elsevier.py` | Financial terms in [`keywords.txt`](scrapers/keywords.txt) were queried and all abstracts from search containing root word 'finance' (e.g. finance, financing, financial) were retrieved. |
| Semantic Scholar | `semantic_scholar.py` | 'Business' and 'Economics'-tagged papers are retrieved. |
| Pubmed (decommissioned) | `pubmed.py` | Financial terms in [`keywords.txt`](scrapers/keywords.txt) were queried and all abstracts from search containing root word 'finance' (e.g. finance, financing, financial) were retrieved. |
| Sagepub (decommissioned) | `sagepub.py` | All abstracts from journals tagged with 'Economic' or 'Management' were retrieved. |

Note that we have decommissioned the Pubmed and Sagepub scrapers as a significant percentage of abstracts retrieved from these sources were not financial-related. 

### Usage
To run each scraper:
```sh
python (scraper_file.py)
```

## Built With
* [Python](https://www.python.org/)