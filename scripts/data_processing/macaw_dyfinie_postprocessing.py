import os
import sys
import ast
import json
import pandas as pd
from pathlib import Path
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

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)
            

# data preprocessing
macaw_to_label_mapping = {
    'direct': 'DIRECT',
    'indirect': 'INDIRECT',
    'not applicable': None,
    'attribute': 'ATTRIBUTE',
    'function': 'FUNCTION',
    'positive': 'POSITIVE',
    'negative': 'NEGATIVE',
    'neutral': 'NEUTRAL',
    'conditional': 'CONDITION',
    'comparison': 'COMPARISON',
    'uncertain': 'UNCERTAIN',
    'unrelated': 'NONE',
}
predictions = ["macaw_1", "macaw_1_sentence", "macaw_1_abstract", "macaw_2", "macaw_2_sentence", "macaw_2_abstract"]

if __name__ == "__main__":
    pred_directories = [
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_comb/external_zhiren/coarse/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_comb/external_zhiren/granular/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/external_zhiren/coarse/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/external_zhiren/granular/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_comb/finance/coarse_coref/",
        # # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_comb/finance/granular_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/finance/coarse_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/finance/granular_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-11b/rel_comb/external_zhiren/coarse/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-11b/rel_comb/external_zhiren/granular/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-11b/rel_perm/external_zhiren/coarse/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-11b/rel_perm/external_zhiren/granular/",
        "data/predictions/macaw/macaw_dyfinie/macaw-11b/rel_comb/finance/coarse_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_comb/finance/granular_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/finance/coarse_coref/",
        # "data/predictions/macaw/macaw_dyfinie/macaw-large/rel_perm/finance/granular_coref/"
    ]
    dyfinie_directories = [
        # "data/predictions/dygiefinbert/external_zhiren/coarse/",
        # "data/predictions/dygiefinbert/external_zhiren/granular/",
        # "data/predictions/dygiefinbert/external_zhiren/coarse/",
        # "data/predictions/dygiefinbert/external_zhiren/granular/",
        # "data/predictions/dygiefinbert/finance/coarse_coref/",
        # "data/predictions/dygiefinbert/finance/granular_coref/",
        # "data/predictions/dygiefinbert/finance/coarse_coref/",
        # "data/predictions/dygiefinbert/finance/granular_coref/",
        # "data/predictions/dygiefinbert/external_zhiren/coarse/",
        # "data/predictions/dygiefinbert/external_zhiren/granular/",
        # "data/predictions/dygiefinbert/external_zhiren/coarse/",
        # "data/predictions/dygiefinbert/external_zhiren/granular/",
        "data/predictions/dygiefinbert/finance/coarse_coref/"
    ]
    save_directories = [
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_comb/external_zhiren/coarse/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_comb/external_zhiren/granular/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_perm/external_zhiren/coarse/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_perm/external_zhiren/granular/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_comb/finance/coarse_coref/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_comb/finance/granular_coref/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_perm/finance/coarse_coref/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-large/rel_perm/finance/granular_coref/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_comb/external_zhiren/coarse/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_comb/external_zhiren/granular/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_perm/external_zhiren/coarse/",
        # "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_perm/external_zhiren/granular/",
        "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_comb/finance/coarse_coref/",
    ]
    dataset_types = ["train", "dev", "test"]

    for i in range(len(pred_directories)):
        pred_dir, dyfinie_dir, save_dir = pred_directories[i], dyfinie_directories[i], save_directories[i]
        for type in dataset_types:
            path = f"{pred_dir}{type}.csv"
            dyfinie_path = f"{dyfinie_dir}{type}.jsonl"
            if not Path(path).exists() or not Path(dyfinie_path):
                continue 
            print(path)
            # retrieve data
            df = pd.read_csv(path)

            # preprocess data
            df['E1_ix'] = df['E1_ix'].apply(lambda x: ast.literal_eval(x))
            df['E2_ix'] = df['E2_ix'].apply(lambda x: ast.literal_eval(x))
            for label in predictions:
                df[label] = df[label].apply(lambda x: macaw_to_label_mapping[x] if x in macaw_to_label_mapping else None)
            max_key = {row["doc_key"]: row["max_docsent_key"] for ind, row in df.iterrows()}

            # extract predicted relations
            relations = { x:{} for x in predictions }
            for doc_key, max_docsent_key in max_key.items():
                abstract_relations = { x:[] for x in predictions }
                for i in range(max_docsent_key):
                    sentence_relations = { x:[] for x in predictions }
                    # filter df
                    filtered_df = df[(df["doc_key"] == doc_key) & (df["docsent_key"] == i)]
                    # extract relations
                    for index, row in filtered_df.iterrows():
                        for pred_type in predictions:
                            if row[pred_type]:
                                pred_rel = (row['E1_ix'][0], row['E1_ix'][1], row['E2_ix'][0], row['E2_ix'][1], row[pred_type])
                                sentence_relations[pred_type].append(pred_rel)
                    # update sentence
                    for pred_type in predictions:
                        abstract_relations[pred_type].append(sentence_relations[pred_type])
                # update relations
                for pred_type in predictions:
                    relations[pred_type][doc_key] = abstract_relations[pred_type]

            # combine with dyfinie
            # load corresponding dyfinbert pred jsonl file
            dyfinbert_df = load_jsonl(dyfinie_path)

            # append relations
            for i in range(len(dyfinbert_df)):
                for pred_type in predictions:
                    try:
                        dyfinbert_df[i][pred_type] = relations[pred_type][dyfinbert_df[i]['doc_key']]
                    except:
                        dyfinbert_df[i][pred_type] = [[] for i in range(len(dyfinbert_df[i]["predicted_relations"]))]
                    combined_relations = []
                    for sent_ix in range(len(dyfinbert_df[i]["predicted_relations"])):
                        combined_relations.append(dyfinbert_df[i][pred_type][sent_ix] + dyfinbert_df[i]["predicted_relations"][sent_ix])
                    dyfinbert_df[i][pred_type + '_dyfinie'] = combined_relations
    
            utils.make_dir(save_dir)
            save_json(f"{save_dir}{type}.jsonl", dyfinbert_df)
