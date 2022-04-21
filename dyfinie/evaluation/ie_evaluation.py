import json
import random
import itertools
from scipy import stats
from pathlib import Path
from relation_metric import SpanRelationMetrics, TokenRelationMetrics

if __name__ == "__main__":
    n_sets = 10
    pred_directories = {
        "openie": {"dataset_names": ["finmechanic/coarse", "finmechanic/granular"], "prob":False},
        "srl": {"dataset_names": ["finmechanic/coarse", "finmechanic/granular"], "prob":False},
        "dyfinie": {"dataset_names": ["finmechanic/coarse", "finmechanic/granular"], "prob":False},
    }

    dataset_types = ["train", "dev", "test"]
    results = {}

    for model, model_params in pred_directories.items():
        prob = model_params["prob"]
        for name in model_params["dataset_names"]:
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
                sample_list = [i for i in range(len(sentence_list))]

                # split into 10 sets
                random.seed(4101)
                k = round(len(sample_list) * 0.5)

                collated_results = {}

                for i in range(n_sets):
                    temp_sample = random.choices(sample_list, k=k)
                    temp_pred = [pred_relation_list[i] for i in temp_sample]
                    temp_gold = [gold_relation_list[i] for i in temp_sample]
                    temp_sentence = [sentence_list[i] for i in temp_sample]

                    # retrieve metric 
                    span_relation_metric = SpanRelationMetrics()
                    span_relation_metric(temp_pred, temp_gold, temp_sentence)
                    token_relation_metric = TokenRelationMetrics(prob=prob)
                    token_relation_metric(temp_pred, temp_gold, temp_sentence)
                    relation_metrics = span_relation_metric.get_metric()
                    relation_metrics.update(token_relation_metric.get_metric())

                    for metric_name, metric_scores in relation_metrics.items():
                        if metric_name not in collated_results:
                            collated_results[metric_name] = { "precision": [], "recall": [], "f1": [] }
                        for score_name, score_value in metric_scores.items():
                            collated_results[metric_name][score_name].append(score_value)
                
                if name + "/" + type not in results:
                    results[name + "/" + type] = { model: collated_results}
                else:
                    results[name + "/" + type][model] = collated_results
    
    metrics = list(results["finance/coarse/train"]["dygiefinbert"].keys())
    for dataset_path, dataset_results in results.items():
        print(dataset_path)
        models = list(dataset_results.keys())
        for model_a, model_b in itertools.combinations(models, 2):
            if model_a in ["dygiefinbert", "dygiebert"] and model_b in ["dygiefinbert", "dygiebert"]:
                print(f"{dataset_path} H1: {model_b} > {model_a}")
                for metric in metrics:
                    model_a_scores = results[dataset_path][model_a][metric]
                    model_b_scores = results[dataset_path][model_b][metric]
                    for type in ["precision", "recall", "f1"]:
                        ttest = stats.ttest_ind(model_b_scores[type], model_a_scores[type], alternative="greater")
                        print(f"{metric} - {type} - {ttest.pvalue} - {ttest.pvalue < 0.05}")
                
        print("---------------------------------------")