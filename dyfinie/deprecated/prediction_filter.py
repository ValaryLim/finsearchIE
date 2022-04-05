'''
DEPRECATED CODE
Pipeline to filter for higher quality relations.
'''
import os
import sys
import spacy
import json 

sys.path.append(os.getcwd())
import utils

nlp_name = 'en_core_web_sm'
nlp = spacy.load(nlp_name) 

def accept_rel(rel, sents, dist = 10):
    e1_1, e1_2, e2_1, e2_2, r, _, _ = rel
    e2_start = max(e1_1, e2_1)
    e1_end = min(e1_2, e2_2)
    
    sentences_str = [' '.join(x) for x in sents]
    
    # elimination of discourse-related verbs (limited to said and presented)
    sentences_lemma = [[tok.lemma for tok in nlp(x)] for x in sentences_str]
    sentences_lemma_combined = sum(sentences_lemma, [])
    rel_lemma_phrase = sentences_lemma_combined[e1_end+1:e2_start]
    rel_lemma_phrase = [True if x in [8685289367999165211, 138130184627603044] else False for x in rel_lemma_phrase]
    if sum(rel_lemma_phrase) > 1:
        return False
    
    # only one verb is allowed between two entities, except auxiliary verbs (be, have and do)
    # use spacy to determine pos of words
    sentences_pos = [[tok.pos_ for tok in nlp(x)] for x in sentences_str]
    sentences_pos_combined = sum(sentences_pos, []) 
    rel_verb_phrase = sentences_pos_combined[e1_end+1:e2_start]
    rel_verb_phrase = [True if 'VERB' in x else False for x in rel_verb_phrase]
    if sum(rel_verb_phrase) > 1:
        return False
    
    # maximum distance between two entities is limited to 10 words
    max_dist = e2_start - e1_end
    if max_dist > dist:
        return False
    
    return True
    
def process_relations(json_list, dist = 10):
    for i in range(len(json_list)):
        doc = json_list[i]
        # generate filtered relations
        filtered_relations = []
        for sent in doc['predicted_relations']:
            filtered_sent = []
            for rel in sent:
                if accept_rel(rel, doc['sentences'], dist):
                    filtered_sent.append(rel)
            filtered_relations.append(filtered_sent)
        # update jsonlist
        json_list[i]['predicted_relations'] = filtered_relations
    return json_list

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)

if __name__ == "__main__":
    pred_dirs = [
        'data/predictions/dygiefinbert/finance/coarse/',
        'data/predictions/dygiefinbert/finance/coarse_coref/',
        'data/predictions/dygiefinbert/finance/granular/',
        'data/predictions/dygiefinbert/finance/granular_coref/',
        'data/predictions/dygiefinbert/external_zhiren/coarse/',
        'data/predictions/dygiefinbert/external_zhiren/coarse_coref/',
        'data/predictions/dygiefinbert/external_zhiren/granular/',
        'data/predictions/dygiefinbert/external_zhiren/granular_coref/',
        'data/predictions/dygiebert/finance/coarse/',
        'data/predictions/dygiebert/finance/coarse_coref/',
        'data/predictions/dygiebert/finance/granular/',
        'data/predictions/dygiebert/finance/granular_coref/',
        'data/predictions/dygiebert/external_zhiren/coarse/',
        'data/predictions/dygiebert/external_zhiren/coarse_coref/',
        'data/predictions/dygiebert/external_zhiren/granular/',
        'data/predictions/dygiebert/external_zhiren/granular_coref/'
    ]

    # read files
    for pred_dir in pred_dirs:
        post_pred_dir = pred_dir.replace("bert", "bert_processed")
        utils.make_dir(post_pred_dir)

        for filename in os.listdir(pred_dir):
            # process predictions
            if ".jsonl" in filename:
                with open(pred_dir + filename) as json_file:
                    json_list = list(json_file)
                    json_list = [json.loads(x) for x in json_list]
                processed_json_list = process_relations(json_list, dist = 10)
            # save jsonl file
            save_json(post_pred_dir + filename, processed_json_list)