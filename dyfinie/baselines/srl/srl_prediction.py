'''
SRL (Baseline) Prediction Pipeline
'''
import os
import sys
import tqdm
import json
import itertools
import numpy as np
from pathlib import Path
from allennlp.predictors.predictor import Predictor

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_ner_relations(cleaned_relations, shift = 0):
    relations_set = set()
    ner_set = set()
    for relation in cleaned_relations:
        arg0_tag = np.where([True if x == 0 else False for x in relation])[0]
        arg1_tag = np.where([True if x == 1 else False for x in relation])[0]
        try:
            arg0_start, arg0_end = min(arg0_tag), max(arg0_tag)
            arg1_start, arg1_end = min(arg1_tag), max(arg1_tag)
            # add entity and relations
            ner_set.add((int(arg0_start + shift), int(arg0_end + shift), "ENTITY"))
            ner_set.add((int(arg1_start + shift), int(arg1_end + shift), "ENTITY"))
            relations_set.add((int(arg0_start + shift), int(arg0_end + shift), int(arg1_start + shift), int(arg1_end + shift), "RELATION"))
        except:
            continue
    ner_list = [list(x) for x in ner_set]
    relation_list = [list(x) for x in relations_set]
    return ner_list, relation_list

def extract_tag(tag):
    if 'ARG0' in tag:
        return 0
    elif 'ARG1' in tag:
        return 1
    else:
        return -1

def clean_pred_tags(gold_tags):
    prev, left_tags, right_tags = -1, gold_tags.copy(), gold_tags.copy()
    
    # left pass
    for i in range(len(gold_tags)):
        if gold_tags[i] == None:
            left_tags[i] = prev
        else:
            left_tags[i] = gold_tags[i]
            prev = gold_tags[i]
            
    # right pass
    prev = -1

    for i in range(len(gold_tags)-1, -1, -1): 
        if gold_tags[i] == None:
            right_tags[i] = prev
        else: 
            right_tags[i] = gold_tags[i]
            prev = gold_tags[i]
    
    cleaned_tags = []
    for i in range(len(gold_tags)):
        if left_tags[i] == right_tags[i]:
            cleaned_tags.append(left_tags[i])
        else:
            cleaned_tags.append(-1)
    
    return cleaned_tags

def format_pred_tags(gold_toks, pred_toks, pred_tags):
    '''
    Parameters:
        gold_toks: tokens from gold-standard labels
        pred_toks: tokens extracted by model
        pred_tags: tags predicted by model
        
    Returns:
        gold_tags: tags predicted by model with index matched to gold_toks
    '''
    # extract gold tags
    offset = 0
    gold_tags = []
    for i in range(len(pred_toks)):
        if pred_toks[i] == gold_toks[i + offset]:
            gold_tags.append(extract_tag(pred_tags[i]))
        else:
            while pred_toks[i] != gold_toks[i + offset]:
                offset += 1
                gold_tags.append(None)
            gold_tags.append(extract_tag(pred_tags[i]))
            
    # clean gold tags by eliminating all "None" instances
    cleaned_tags = clean_pred_tags(gold_tags)

    return cleaned_tags

def save_jsonl(file_path, data_list):
    with open(file_path, "w") as f:
        for data in data_list:
            print(json.dumps(data), file=f)

if __name__ == "__main__":
    predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/structured-prediction-srl-bert.2020.12.15.tar.gz")

    # retrieve data
    raw_json_file = sys.argv[1]
    pred_data_path = sys.arg[2]

    # create directory for prediction
    make_dir(pred_data_path)

    # generate pred_data_file name
    pred_data_file = f"{pred_data_path}/{raw_json_file.split('/')[-1]}l"

    # read json file
    with open(path, "r") as json_file:
        json_list = list(json_file)

    preds = []
    # predict for each abstract
    for json_row in tqdm.tqdm(json_list):
        abstract = json.loads(json_row)
        predicted_ner, predicted_relations = [], []
        # extract sentences
        sentences_tok = abstract["sentences"]
        sentences_str = [" ".join(x) for x in sentences_tok]
        sentences_len = [0] + [len(x) for x in sentences_tok]
        sentences_len_cumsum = list(np.cumsum(sentences_len))

        for i in range(len(sentences_tok)):
            sentence = sentences_str[i]
            gold_tok = sentences_tok[i]
            shift = sentences_len_cumsum[i]

            # predict
            pred_sentence = predictor.predict(sentence=sentence)
            pred_tok = pred_sentence['words']

            # extract relations 
            cleaned_relations = []
            for relation in pred_sentence["verbs"]:
                pred_rel_tags = relation["tags"]
                pred_rel_tags = format_pred_tags(gold_tok, pred_tok, pred_rel_tags)
                cleaned_relations.append(pred_rel_tags)

            sentence_ner, sentence_relations = extract_ner_relations(cleaned_relations, shift = shift)

            predicted_ner.append(sentence_ner)
            predicted_relations.append(sentence_relations)
            
        row_pred = {
            "doc_key": abstract["doc_key"],
            "dataset": '_'.join(dname.split('/')),
            "sentences": abstract["sentences"],
            "ner": abstract["ner"],
            "relations": abstract["relations"],
            "predicted_ner": predicted_ner,
            "predicted_relations": predicted_relations
        }
        preds.append(row_pred)
    
    save_jsonl(pred_data_file, preds)


