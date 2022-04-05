import json
import pandas as pd
import numpy as np

datasets = [
    "data/prodigy_processed/external_zhiren/coarse/test.json", \
    "data/prodigy_processed/finance/coarse/all.json", \
    "data/prodigy_processed/finance/coarse/train.json"
]

if __name__ == "__main__":
    for dataset_path in datasets:
        # retrieve data
        data = []
        with open(dataset_path, "r") as jsonlfile:
            for line in jsonlfile:
                data.append(json.loads(line))
        
        # get average length of tokens
        length, n = 0, 0
        for row in data:
            for sentence in row["ner"]:
                for token in sentence:
                    length += (token[1] - token[0] + 1)
                    n += 1 
        print(f"{dataset_path} avg length of token = {length/n}")