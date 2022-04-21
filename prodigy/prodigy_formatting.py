'''
Processes model output into format accepted by prodigy
'''
import os
import sys
import json
import copy

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

def make_dir(filedir):
    if not os.path.exists(filedir):
        os.makedirs(filedir)

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

def format_data(pred_data, raw_data, gold=False):
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
    prediction_data_file = sys.argv[1]
    raw_data_file = sys.argv[2]
    formatted_data_path = sys.argv[3]
    
    # read predicted data path
    pred_data = load_pred_data(prediction_data_file)

    # read raw data
    raw_data = load_raw_data(raw_data_file)

    # format predicted data
    formatted_pred_data = format_data(pred_data, raw_data, gold=False)
    formatted_gold_data = format_data(pred_data, raw_data, gold=True)

    # save as json file
    gold_path = f"{formatted_data_path}/gold.json"
    pred_path = f"{formatted_data_path}/pred.json"
    make_dir(formatted_data_path)
    save_json(gold_path, formatted_pred_data)
    save_json(pred_path, formatted_gold_data)
