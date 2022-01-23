import os
import sys
import json
import pandas as pd
import numpy as np
from itertools import combinations, permutations
# set working directory
sys.path.append(os.getcwd())
import utils

def load_jsonl(path):
    raw_data = []
    with open(path, "r") as jsonlfile:
        for line in jsonlfile:
            # read line
            json_line = json.loads(line)
            raw_data.append(json_line)
    return raw_data

def identify_relation(pair, rel_dict, comb=True):
    if pair in rel_dict:
        return rel_dict[pair]
    elif comb and (pair[1], pair[0]) in rel_dict:
        return rel_dict[pair[1], pair[0]]
    else:
        return ''

def macaw_processing(jsonl_path):
    df = load_jsonl(jsonl_path)

    comb_all, perm_all, coref_all = [], [], []

    for abstract in df:
        abstract_text_list = sum(abstract['sentences'], [])
        abstract_text = ' '.join(abstract_text_list)
        abstract_key = abstract['doc_key']
        full_ner_list = []
        
        # GENERATE ALL POSSIBLE RELATIONS
        for i in range(len(abstract['sentences'])): 
            sentence, ner_list, rel_list = abstract['sentences'][i], abstract['predicted_ner'][i], abstract['predicted_relations'][i]
            sentence_text = ' '.join(sentence)
            # generate ner pairs
            ner_list = [(' '.join(abstract_text_list[x[0]:x[1]+1]), (x[0], x[1])) for x in ner_list] # clean ner_list
            comb_ner_pairs = list(combinations(ner_list, 2))
            perm_ner_pairs = list(permutations(ner_list, 2))
            # process relations (into dict)
            rel_dict = {(' '.join(abstract_text_list[x[0]:x[1]+1]), ' '.join(abstract_text_list[x[2]:x[3]+1])): x[4] for x in rel_list}
            # label each perm_pair and combi_pair with relation
            comb_ner_pairs = [[pair[0], pair[1], identify_relation((pair[0][0], pair[1][0]), rel_dict)] for pair in comb_ner_pairs]
            perm_ner_pairs = [[pair[0], pair[1], identify_relation((pair[0][0], pair[1][0]), rel_dict, comb=False)] for pair in perm_ner_pairs]
            # update relation dicts
            for comb_pair in comb_ner_pairs:
                comb_all.append({
                    'E1': comb_pair[0][0], 'E2': comb_pair[1][0], 'R_DyFinIE': comb_pair[2],
                    'E1_ix': comb_pair[0][1], 'E2_ix': comb_pair[1][1],
                    'sentence': sentence_text, 'abstract': abstract_text, 'doc_key': abstract_key, 'docsent_key': i, 'max_docsent_key':len(abstract['sentences'])
                })
            for perm_pair in perm_ner_pairs:
                perm_all.append({
                    'E1': perm_pair[0][0], 'E2': perm_pair[1][0], 'R_DyFinIE': perm_pair[2], 
                    'E1_ix': perm_pair[0][1], 'E2_ix': perm_pair[1][1],
                    'sentence': sentence_text, 'abstract': abstract_text, 'doc_key': abstract_key, 'docsent_key': i, 'max_docsent_key':len(abstract['sentences'])
                })
            # update ner list
            full_ner_list.extend(ner_list)
            
        # GENERATE ALL POSSIBLE COREFERENCES
        # generate ner pairs
        coref_ner_pairs = list(combinations(full_ner_list, 2))
        coref_dict = { x:0 for x in coref_ner_pairs }
        for coref_cluster in abstract['clusters']:
            cluster_ner_list = [' '.join(abstract_text_list[x[0]:x[1]+1]) for x in coref_cluster]
            cluster_ner_pairs_list = list(combinations(cluster_ner_list, 2))
            for cluster_pair in cluster_ner_pairs_list:
                coref_dict[cluster_pair] = 1
        for pair, pair_coref in coref_dict.items():
            coref_all.append({
                'E1': pair[0][0], 'E2': pair[1][0], 'C_DyFinIE': pair_coref, 
                'E1_ix': pair[0][1], 'E2_ix': pair[1][1],
                'abstract': abstract_text, 'doc_key': abstract_key, 'docsent_key': i, 'max_docsent_key':len(abstract['sentences'])
            })

    comb_df, perm_df, coref_df = pd.DataFrame(comb_all), pd.DataFrame(perm_all), pd.DataFrame(coref_all)
    
    return comb_df, perm_df, coref_df

if __name__ == "__main__":
    source_path = "data/predictions/dygiefinbert/"
    destination_path = "data/macaw/macaw_dyfinie/"
    data_directories = ["finance/coarse_coref/", "finance/granular_coref/", "external_zhiren/coarse/", "external_zhiren/granular/"]
    
    # retrieve all data files
    for dir in data_directories:
        # create output directories
        for type in ["rel_comb/", "rel_perm/", "coref/"]:
            utils.make_dir(destination_path + type + dir)
        
        # retrieve all datasets
        for file in os.listdir(source_path + dir):
            comb_df, perm_df, coref_df = macaw_processing(source_path + dir + file)
            print(destination_path + 'rel_comb/' + dir + file.split('.')[0] + '.csv')
            comb_df.to_csv(destination_path + 'rel_comb/' + dir + file.split('.')[0] + '.csv', index=False)
            perm_df.to_csv(destination_path + 'rel_perm/' + dir + file.split('.')[0] + '.csv', index=False)
            coref_df.to_csv(destination_path + 'coref/' + dir + file.split('.')[0] + '.csv', index=False)