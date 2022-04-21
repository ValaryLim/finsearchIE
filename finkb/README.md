# FinKB
FinKB (Financial Knowledge Base) is a Financial Mechanism Knowledge Base that consists of 646,977 coarse relational triplets and 391,843 granular relational triplets, extracted by our custom information extraction model, DyFinIE.

## Relation Schema
### Coarse Relation Schema
| Relation Label | Description |
| --- | --- |
| DIRECT | E1 is an ATTRIBUTE/SUBSET/FUNCTION/MODEL of E2 |
| INDIRECT | E1 INFLUENCES/CORRELATES with E2 |

### Granular Relation Schema
| Relation Label | Description |
| --- | --- |
| ATTRIBUTE | E1 is an ATTRIBUTE/SUBSET of E2 |
| FUNCTION | E1 is a FUNCTION/MODEL of E2 |
| POSITIVE | E1 POSITIVELY correlates with/causes E2 |
| NEGATIVE | E1 NEGATIVELY correlates with/causes E2 |
| NEUTRAL | E1 correlates with/causes E2 (no direction indicated) |
| NONE | E1 does not correlate with/cause E2 |
| CONDITION | E1 is a CONDITION of E2 |
| COMPARISON | E1 is DIFFERENT/BETTER than E2 |
| UNCERTAIN | E1 and E2 have UNCERTAIN relationship |

## Getting Started
### Prerequisites
This project was built to run on Python 3.9. Refer to the [Python Installation Guide](https://www.python.org/downloads/) for more instructions. Alternatively, if Anaconda is installed, a separate conda environment can be created using the following:
```bash
conda create -n finkb python=3.9
```

### Installation
1. Clone the repository
   ```sh
   git clone https://github.com/ValaryLim/finsearchIE.git
   ```
2. Move into the FinKB directory
    ```sh
    cd finsearchIE/finkb/
    ```
3. Install Python packages
    ```sh
    pip install -r requirements.txt
    ```

## Generate FinKB
1. Move into the FinSearch directory
    ```sh
    cd finsearchIE
    ```
2. Run FinKB generation script
    ```sh
    python finkb/finkb_generation.py
    ```

## Analyse FinKB
We provide an analysis script to compute basic statistics (number of relations, number of words per entity). To run the script:
1. Move into the FinSearch directory
    ```sh
    cd finsearchIE
    ```
2. Run FinKB generation script
    ```sh
    python finkb/finkb_analysis.py
    ```