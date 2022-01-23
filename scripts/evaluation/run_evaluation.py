import json
import pandas as pd
from pathlib import Path
from relation_metric import SpanRelationMetrics, TokenRelationMetrics

if __name__ == "__main__":
    pred_directories = {
        "openie": {"dataset_names": ["finance/coarse", "finance/granular", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False},
        "srl": {"dataset_names": ["finance/coarse", "finance/granular", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False},
        "dygiebert": {"dataset_names": ["finance/coarse", "finance/granular", "finance/coarse_coref", "finance/granular_coref", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False},
        "dygiefinbert": {"dataset_names": ["finance/coarse", "finance/granular", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False},
        "dygiebert_processed": {"dataset_names": ["finance/coarse", "finance/granular", "finance/coarse_coref", "finance/granular_coref", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False},
        "dygiefinbert_processed": {"dataset_names": ["finance/coarse", "finance/granular", "finance/coarse_coref", "finance/granular_coref", "external_zhiren/coarse", "external_zhiren/granular"], "prob":False}
    }

    dataset_types = ["train", "dev", "test"]

    for model, model_params in pred_directories.items():
        prob = model_params["prob"]
        for name in model_params["dataset_names"]:
            relation_metrics_dict = {}
            for type in dataset_types:
                path = f"data/predictions/{model}/{name}/{type}.jsonl"
                if not Path(path).exists():
                    continue
                
                # retrieve data
                data = []
                with open(path, "r") as jsonlfile:
                    for line in jsonlfile:
                        data.append(json.loads(line))
                
                # retrieve pred and gold relations
                pred_relation_list = [x["predicted_relations"] for x in data]
                gold_relation_list = [x["relations"] for x in data]
                sentence_list = [x["sentences"] for x in data]

                # retrieve metric 
                span_relation_metric = SpanRelationMetrics()
                span_relation_metric(pred_relation_list, gold_relation_list, sentence_list)
                token_relation_metric = TokenRelationMetrics(prob=prob)
                token_relation_metric(pred_relation_list, gold_relation_list, sentence_list)
                relation_metrics = span_relation_metric.get_metric()
                relation_metrics.update(token_relation_metric.get_metric())

                relation_metrics_dict[type] = pd.DataFrame(relation_metrics)
            
            # write results to excel
            joint_name = "_".join(name.split("/"))
            with pd.ExcelWriter(f"data/evaluations/{model}_{joint_name}.xlsx") as writer:
                for sheet_name, relation_metrics_df in relation_metrics_dict.items():
                    relation_metrics_df.to_excel(writer, sheet_name=sheet_name)
