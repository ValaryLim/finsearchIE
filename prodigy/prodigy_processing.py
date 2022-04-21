import os
import sys
import json
import tqdm
import glob
import spacy
import random
import numpy as np
import pandas as pd

GRANULAR_TO_COARSE = {
    'ATTRIBUTE': 'DIRECT',
    'FUNCTION': 'DIRECT',
    'POSITIVE': 'INDIRECT',
    'NEGATIVE': 'INDIRECT',
    'NEUTRAL': 'INDIRECT',
    'NONE': 'INDIRECT',
    'UNCERTAIN': 'INDIRECT',
    'CONDITION': 'INDIRECT',
    'COMPARISON': 'INDIRECT'
}

def make_dir(filedir):
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    
def granular_to_coarse(relations):
    coarse_relations = []
    for rel_sentence in relations:
        coarse_rel_sentence = []
        for rel in rel_sentence:
            coarse_rel_sentence.append([rel[0], rel[1], rel[2], rel[3], GRANULAR_TO_COARSE[rel[4]]])
        coarse_relations.append(coarse_rel_sentence)
    return coarse_relations

def unpack_entities(entities, sentences_index):
    ner = [[] for i in range(len(sentences_index) - 1)]
    for entity in entities:
        token_start = entity['token_start']
        token_end = entity['token_end']
        # identify which sentence entity belongs to
        token_sentence_no = np.argmax(np.array(sentences_index) > token_start) - 1
        # dump into correct sentence
        # print(sentences_index, token_start, token_end, token_sentence_no)
        if token_end < sentences_index[token_sentence_no + 1]:
            ner[token_sentence_no].append([token_start, token_end, 'ENTITY'])
    return ner

def unpack_relations(relations_unprocessed, sentences_index, ner):
    relations = [[] for i in range(len(sentences_index) - 1)]
    coref_graph = {}
    for relation in relations_unprocessed:
        head_token_start = relation['head_span']['token_start']
        head_token_end = relation['head_span']['token_end']
        child_token_start = relation['child_span']['token_start']
        child_token_end = relation['child_span']['token_end']
        relation_label = relation['label']
        
        if relation_label != 'COREFERENCE':
            # record relation
            token_sentence_no = np.argmax(np.array(sentences_index) > head_token_start) - 1
            if ([child_token_start, child_token_end, 'ENTITY'] in ner[token_sentence_no]) and ([head_token_start, head_token_end, 'ENTITY'] in ner[token_sentence_no]): 
                relations[token_sentence_no].append([head_token_start, head_token_end, child_token_start, child_token_end, relation_label])
        else:
            # record coreference
            key = (head_token_start, head_token_end)
            value = (child_token_start, child_token_end)
            if key in coref_graph:
                coref_graph[key].append(value)
            else:
                coref_graph[key] = [value,]
            if value in coref_graph:
                coref_graph[value].append(key)
            else:
                coref_graph[value] = [key,]
    return relations, coref_graph

def unpack_clusters(coref_graph):
    all_nodes = set(coref_graph.keys())
    unvisited_nodes = set(coref_graph.keys())
    clusters = []

    for parent_node in all_nodes:
        if parent_node in unvisited_nodes:
            curr_cluster, queue = [], []
            unvisited_nodes.remove(parent_node)
            curr_cluster.append(parent_node)
            queue.append(parent_node)

            while len(queue) > 0:
                curr_node = queue.pop()
                for node in coref_graph[curr_node]:
                    if node in unvisited_nodes:
                        queue.append(node)
                        curr_cluster.append(node)
                        unvisited_nodes.remove(node)
            clusters.append(curr_cluster)
        else:
            continue # do nothing
    return clusters

def process_abstract_list(abstract_list):
    abstract_df = pd.DataFrame(abstract_list)
    # get unique abstracts
    abstract_df = abstract_df.drop_duplicates(subset=['doc_key'])
    # convert back to list
    filtered_abstract_list = abstract_df.to_dict('records')

    return filtered_abstract_list

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)

if __name__ == "__main__": 
    annotated_dir = sys.argv[1]
    processed_dir = sys.argv[2]

    # load nlp model
    nlp_name='en_core_web_sm'
    nlp = spacy.load(nlp_name) 

    granular_abstract_list, coarse_abstract_list = [], []

    for annotated_jsonl_path in glob.glob(f"{annotated_dir}/*.jsonl"):
        with open(annotated_jsonl_path, 'r') as json_file:
            json_list = list(json_file)

        for json_str in tqdm.tqdm(json_list):
            # load sample
            sample = json.loads(json_str)

            # reject if sample is not accepted
            if sample['answer'] != 'accept': # ignore
                continue
            
            # retrieve sample information
            doc_id = sample['meta']['id']
            text = sample['text']
            
            # tokenize text
            text_doc = nlp(text)
            sentences = [[tok.text for tok in sent] for sent in text_doc.sents]
            sentences_index = [len(x) for x in sentences]
            sentences_index = [0] + list(np.cumsum(sentences_index))
            
            # tag entities
            entities = sample['spans']
            ner = unpack_entities(entities, sentences_index)
            
            # tag relations
            relations_unprocessed = sample['relations']
            granular_relations, coref_graph = unpack_relations(relations_unprocessed, sentences_index, ner)
            coarse_relations = granular_to_coarse(granular_relations)
            
            # tag clusters
            clusters = unpack_clusters(coref_graph)
            
            granular_dict = {
                'clusters': clusters,
                'sentences': sentences,
                'ner': ner,
                'relations': granular_relations,
                'doc_key': doc_id
            }

            coarse_dict = {
                'clusters': clusters,
                'sentences': sentences,
                'ner': ner,
                'relations': coarse_relations,
                'doc_key': doc_id
            }

            granular_abstract_list.append(granular_dict)
            coarse_abstract_list.append(coarse_dict)
    
    # remove duplicates
    filtered_granular_abstract_list = process_abstract_list(granular_abstract_list)
    filtered_coarse_abstract_list = process_abstract_list(coarse_abstract_list)

    # dump data
    processed_datasets = {
        'finmechanic_granular': filtered_granular_abstract_list,
        'finmechanic_coarse': filtered_coarse_abstract_list
    }

    # derive train and test mask
    random.seed(4101)
    random_mask = [random.uniform(0,1) for i in range(len(filtered_granular_coref_abstract_list))]
    train_mask = [(x > 0.4) for x in random_mask]
    dev_mask = [((x <= 0.4) & (x > 0.2)) for x in random_mask]
    test_mask = [(x <= 0.2) for x in random_mask]

    # save processed datasets
    for file_dir, abstract_list in processed_datasets.items():
        # train and test set
        train_set = [x for x, y in zip(abstract_list, train_mask) if y]
        dev_set = [x for x, y in zip(abstract_list, dev_mask) if y]
        test_set = [x for x, y in zip(abstract_list, test_mask) if y]
        # save jsons
        save_dir = f"{processed_dir}/{file_dir}"
        make_dir(save_dir)
        save_json(f'{save_dir}/all.json', abstract_list)
        save_json(f'{save_dir}/train.json', train_set)
        save_json(f'{save_dir}/dev.json', dev_set)
        save_json(f'{save_dir}/test.json', test_set)
