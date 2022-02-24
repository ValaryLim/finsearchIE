import json
import ast
import pandas as pd

def load_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

def load_jsonl(filename):
    with open(filename, 'r') as jsonl_file:
        data = list(jsonl_file)
        data = [json.loads(x) for x in data]
    return data

def load_csv(filename, list_cols=[]):
    converters = { x : ast.literal_eval for x in list_cols }
    data = pd.read_csv(filename, converters=converters)
    return data
