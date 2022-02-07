import os
import json

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_json(file_path, abstract_list):
        with open(file_path, "w") as f:
            for abstract in abstract_list:
                print(json.dumps(abstract), file=f)