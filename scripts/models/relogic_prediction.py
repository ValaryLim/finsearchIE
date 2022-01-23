'''
Pipeline to run pre-trained SRL model from https://github.com/Impavidity/relogic
To run this pipeline:
1. git clone https://github.com/Impavidity/relogic
2. create new conda environment for relogic `conda create --name relogic python=3.7`
3. `pip install -r srl_requirements.txt` from requirements directory
4. python srl_prediction.py
'''
import itertools
import json
from pathlib import Path
from relogic.pipelines.core import Pipeline
from relogic.structures.sentence import Sentence

# load pipeline
pipeline = Pipeline(
  component_names=["predicate_detection", "srl"],
  component_model_names= {"predicate_detection" : "spacy" ,"srl": "srl-conll12"})

def is_arg(arg):
    try:
        arg_num = int(arg.split('ARG')[1])
        return True
    except:
        return False

def parse_srl_relation(relation):
    args = []
    for arg in relation:
        arg_start, arg_end, arg_type = arg[0], arg[1] - 1, arg[2]
        if is_arg(arg[2]):
            args.append([arg_start, arg_end])
    if len(args) >= 2:
        return args[0], args[1]
    return None, None

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)
  
if __name__ == "__main__":
    # retrieve list of jsonfiles 
    dataset_names = ["finance/coarse", "finance/granular", "external_zhiren/coarse", "external_zhiren/granular"]
    dataset_types = ["train", "dev", "test"]
    dataset_paths = []
    for name, type in itertools.product(dataset_names,dataset_types):
        path = f"data/raw_data/{name}/{type}.json"
        if not Path(path).exists():
            continue
        pred_path = f"data/pred_data/{name}/{type}.jsonl"
        preds = []

        # read jsonfile
        with open(path, "r") as json_file:
            json_list = list(json_file)

        for json_row in json_list:
            abstract = json.loads(json_row)

            # retrieve sentences
            sentences = [" ".join(x) for x in abstract["sentences"]]
            
            # run SRL
            ner, relations = [], []
            for sentence in sentences:
                sent = Sentence(text=sentence)
                pipeline.execute([sent])
                sentence_ner, sentence_relations = [], []
                for relation in sent.srl_labels:
                    arg0, arg1 = parse_srl_relation(relation)
                    if arg0 and arg1:
                        sentence_relations.append([arg0[0], arg0[1], arg1[0], arg1[1], "SRL"])
                        sentence_ner.append((arg0[0], arg0[1], "ENTITY"))
                        sentence_ner.append((arg1[0], arg1[1], "ENTITY"))
                sentence_ner = list(set(sentence_ner))
                sentence_ner = [list(x) for x in sentence_ner]
                ner.append(sentence_ner)
                relations.append(sentence_relations)

            row_pred = {
                "doc_key": abstract["doc_key"],
                "dataset": '_'.join(name.split('/')),
                "sentences": abstract["sentences"],
                "ner": abstract["ner"],
                "relations": abstract["relations"],
                "predicted_ner": ner,
                "predicted_relations": relations
            }
            preds.append(row_pred)
        
        # save as jsonl
        save_json(pred_path, preds)
