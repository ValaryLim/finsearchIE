import os
import sys
import json
import pandas as pd
from pathlib import Path
from relation_metric import SpanRelationMetrics, TokenRelationMetrics
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

if __name__ == "__main__":
    pred_directories = [
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
        "data/predictions/macaw_processed/macaw_dyfinie/macaw-11b/rel_comb/finance/coarse_coref/"
    ]
    dataset_types = ["train", "dev", "test"]
    pred_types = ["predicted_relations", "macaw_1", "macaw_1_sentence", "macaw_1_abstract", "macaw_2", 
    "macaw_2_sentence", "macaw_2_abstract", "macaw_1_dyfinie", "macaw_1_sentence_dyfinie", 
    "macaw_1_abstract_dyfinie", "macaw_2_dyfinie", "macaw_2_sentence_dyfinie", "macaw_2_abstract_dyfinie"]
    
    for pred_dir in pred_directories:
        relation_metrics_dict = {}
        for type in dataset_types:
            path = f"{pred_dir}{type}.jsonl"
            if not Path(path).exists():
                continue 
            print(path)
            # retrieve data
            data = load_jsonl(path)

            # retrieve predicted and gold labels
            pred_relation_list = { pred_type:[row[pred_type] for row in data] for pred_type in pred_types }
            gold_relation_list = [x["relations"] for x in data]
            sentence_list = [x["sentences"] for x in data]

            for pred_type in pred_types:
                span_relation_metric = SpanRelationMetrics()
                span_relation_metric(pred_relation_list[pred_type], gold_relation_list, sentence_list)
                relation_metrics = span_relation_metric.get_metric()
                relation_metrics_dict[pred_type + "_" + type] = pd.DataFrame(relation_metrics)
        
            # write results to excel
            utils.make_dir(f"data/evaluations/macaw_processed/macaw_dyfinie/macaw-11b/")
            with pd.ExcelWriter(f"data/evaluations/macaw_processed/macaw_dyfinie/macaw-11b/{'_'.join(pred_dir[59:-1].split('/'))}.xlsx") as writer:
                for sheet_name, relation_metrics_df in relation_metrics_dict.items():
                    relation_metrics_df.to_excel(writer, sheet_name=sheet_name)