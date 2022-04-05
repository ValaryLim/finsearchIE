'''
Processes model output into format accepted by prodigy
'''
import os
import sys
import json
import copy
import tqdm
import numpy as np
import pandas as pd

# set working directory
sys.path.append(os.getcwd())
import utils

# set colors
REL_COLORS = {
    "DIRECT": "#c5bdf4",
    "INDIRECT": "#abc4ff",
    "ATTRIBUTE": "#c5bdf4",
    "FUNCTION": "#eac4d5",
    "POSITIVE": "#adf7b6",
    "NEGATIVE": "#ffc09f",
    "NEUTRAL": "#a0ced9",
    "NONE": "#fcf5c7",
    "CONDITION": "#eeddd3",
    "COREFERENCE": "#809bce",
    "COMPARISON": "#ccdbfd",
    "UNCERTAIN": "#abc4ff",
    "RELATION": "#d1d1d1"
}

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)

def load_raw_data(raw_prodigy_paths):
    raw_data = {}
    for path in raw_prodigy_paths:
        with open(path, "r") as jsonlfile:
            for line in jsonlfile:
                # read line
                json_line = json.loads(line)
                # add to raw data
                if json_line["answer"] == "accept":
                    raw_data[json_line["meta"]["id"]] = json_line
    return raw_data

def load_pred_data(pred_path):
    pred_data = []
    with open(pred_path, "r") as jsonlfile:
        for line in jsonlfile:
            pred_data.append(json.loads(line))
    return pred_data

def format_data(pred_data, raw_dat, gold=False):
    # format predictions suitable for prodigy
    formatted_data = []
    for pred in pred_data:
        # find raw data 
        if gold:
            ner_key, relation_key = "ner", "relations"
        else:
            ner_key, relation_key = "predicted_ner", "predicted_relations"

        raw = copy.deepcopy(raw_data[pred["doc_key"]])
        raw_tokens = raw["tokens"]
        
        formatted_spans, formatted_relations = [], []

        # compute spans
        for sentence in pred[ner_key]:
            for entity in sentence:
                try:
                    token_start, token_end, label = entity
                except:
                    token_start, token_end, label, _, _ = entity
                char_start = raw_tokens[token_start]["start"]
                char_end = raw_tokens[token_end]["end"]
                formatted_spans.append({
                    "start": int(char_start), "end": int(char_end), 
                    "token_start": int(token_start), "token_end": int(token_end),
                    "label": label
                })
        
        # compute relations
        for sentence in pred[relation_key]:
            for relation in sentence:
                try:
                    head_token_start, head_token_end, child_token_start, child_token_end, label = relation
                except:
                    head_token_start, head_token_end, child_token_start, child_token_end, label, _, _ = relation
                head_char_start, head_char_end = raw_tokens[head_token_start]["start"], raw_tokens[head_token_end]["end"]
                child_char_start, child_char_end = raw_tokens[child_token_start]["start"], raw_tokens[child_token_end]["end"]
                formatted_relations.append({
                    "head": int(head_token_end), "child": int(child_token_end), 
                    "head_span": {"start": int(head_char_start), "end": int(head_char_end), "token_start": int(head_token_start), "token_end": int(head_token_end), "label": "ENTITY"},
                    "child_span": {"start": int(child_char_start), "end": int(child_char_end), "token_start": int(child_token_start), "token_end": int(child_token_end), "label": "ENTITY"},
                    "color": REL_COLORS[label],
                    "label": label
                })

        raw["spans"] = formatted_spans
        raw["relations"] = formatted_relations

        formatted_data.append(raw)
    
    return formatted_data

if __name__ == "__main__": 
    model_names = ['openie', 'srl', 'dygiebert', 'dygiefinbert']
    dataset_names = {
        'external_zhiren': {
            'dataset_types': ['coarse/test.jsonl', 'coarse_coref/test.jsonl', 'granular/test.jsonl', 'granular_coref/test.jsonl'],
            'raw_prodigy_paths': ['data/prodigy_raw/external_zhiren.jsonl']
        },
        'finance': {
            'dataset_types': [
                'coarse/train.jsonl', 'coarse/test.jsonl', 'coarse/dev.jsonl', \
                'granular/train.jsonl', 'granular/test.jsonl', 'granular/dev.jsonl', \
                'coarse_coref/train.jsonl', 'coarse_coref/test.jsonl', 'coarse_coref/dev.jsonl', \
                'granular_coref/train.jsonl', 'granular_coref/test.jsonl', 'granular_coref/dev.jsonl'
            ],
            'raw_prodigy_paths': ['data/prodigy_raw/finance_granular_1.jsonl', 'data/prodigy_raw/finance_granular_2.jsonl']
        }
    }
    
    for model in model_names:
        for dataset_name, dataset_dict in dataset_names.items():
            # read raw prodigy paths
            raw_prodigy_paths = dataset_dict['raw_prodigy_paths']
            raw_data = load_raw_data(raw_prodigy_paths)

            dataset_types = dataset_dict['dataset_types']
            pred_paths = [f"data/predictions/{model}/{dataset_name}/{x}" for x in dataset_types]
            save_pred_dirs = [f"data/prodigy_predictions/{model}/{dataset_name}/{x.split('/')[0]}/" for x in dataset_types]
            save_gold_dirs = [f"data/prodigy_gold_predictions/{model}/{dataset_name}/{x.split('/')[0]}/" for x in dataset_types]
            save_pred_paths = [f"data/prodigy_predictions/{model}/{dataset_name}/{x}" for x in dataset_types]
            save_gold_paths = [f"data/prodigy_gold_predictions/{model}/{dataset_name}/{x}" for x in dataset_types]
            
            for i in range(len(dataset_types)):
                print(pred_paths[i])
                # read predictions
                pred_data = load_pred_data(pred_paths[i])

                # format predicted data
                formatted_pred_data = format_data(pred_data, raw_data, gold=False)
                formatted_gold_data = format_data(pred_data, raw_data, gold=True)

                # save as json file
                utils.make_dir(save_pred_dirs[i])
                utils.make_dir(save_gold_dirs[i])
                save_json(save_pred_paths[i], formatted_pred_data)
                save_json(save_gold_paths[i], formatted_gold_data)
