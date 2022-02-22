import os
import json

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)

def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def load_jsonl(file_path):
    raw_data = []
    with open(file_path, "r") as f:
        for line in f:
            # read line
            json_line = json.loads(line)
            raw_data.append(json_line)
    return raw_data