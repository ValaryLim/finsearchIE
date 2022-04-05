'''
Utilities Package
Loads and Saves Data and Models
'''
import ast
import json
import joblib
import numpy as np
import pandas as pd

def load_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

def load_jsonl(filename):
    print("Loading...", filename)
    with open(filename, 'r') as jsonl_file:
        data = list(jsonl_file)
        data = [json.loads(x) for x in data]
    return data

def save_jsonl(file_path, data_list):
    with open(file_path, "w") as f:
        for data in data_list:
            print(json.dumps(data), file=f)

def load_csv(filename, list_cols=[]):
    converters = { x : ast.literal_eval for x in list_cols }
    data = pd.read_csv(filename, converters=converters)
    return data

def save_numpy(filename, numpy_array):
    np.save(filename, numpy_array)

def load_numpy(filename):
    print("Loading...", filename)
    return np.load(filename)

def save_pkl(filename, model):
    joblib.dump(model, filename)

def load_pkl(filename):
    return joblib.load(filename)
