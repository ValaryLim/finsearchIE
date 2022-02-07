# this file is to generate finkb (using many different models)
import json
import encoder
import sys 
import os
# set working directory
sys.path.append(os.getcwd())
import utils

# load jsonl files
RAW_PATHS = [
    "data/predictions/finkb/finance_coarse_coref.jsonl", 
    "data/predictions/finkb/finance_granular_coref.jsonl"
]
PROC_PATHS = [
    "data/finkb/finance_coarse_coref.jsonl", 
    "data/finkb/finance_granular_coref.jsonl"
]
SENT_PATHS = [
    "data/finkb/finance_coarse_sents.json", 
    "data/finkb/finance_granular_sents.json"
]
MODELS = {
    # 'finkb': 'ProsusAI/finbert',
    # 'multiqakb': 'multi-qa-MiniLM-L6-cos-v1',
    # 'msmarcokb': 'msmarco-MiniLM-L6-cos-v5',
    'stsbroberta': 'stsb-roberta-large'
}

class FinKBGenerator:
    def __init__(self, model_name):
        self.encoder = encoder.Encoder(model_name)
    
    def extract_relations(self, json_list):
        extracted_rels = [] # fields: E1 E2 REL DOC_KEY E1_START E1_END E2_START E2_END

        for abstract in json_list:
            # combine sentences
            combined_sentences = sum(abstract["sentences"], [])

            # extract relations
            for sentence_relations in abstract["predicted_relations"]:
                for rel in sentence_relations:
                    # process relation
                    e1_start, e1_end, e2_start, e2_end, r = rel[0], rel[1], rel[2], rel[3], rel[4]
                    e1_str = " ".join(combined_sentences[e1_start:e1_end+1])
                    e2_str = " ".join(combined_sentences[e2_start:e2_end+1])

                    # update extracted relations list
                    extracted_rels.append({
                        "E1": e1_str, 
                        "E2": e2_str,
                        "E1_CODE": self.encoder.encode_entity(e1_str),
                        "E2_CODE": self.encoder.encode_entity(e2_str),
                        "E1_START": e1_start, 
                        "E1_END": e1_end, 
                        "E2_START": e2_start, 
                        "E2_END": e2_end, 
                        "REL": r,
                        "DOC_KEY": abstract["doc_key"]
                    })

        return extracted_rels

    def extract_sentences(self, json_list):
        sentence_dict = {}
        for abstract in json_list:
            # combine sentences
            combined_sentences = sum(abstract["sentences"], [])
            # update sentence dict
            sentence_dict[abstract["doc_key"]] = combined_sentences
        return sentence_dict

if __name__ == "__main__":
    for model_code, model_name in MODELS.items():
        print("Generating output for model:", model_code)

        # generate directory name
        utils.make_dir("data/" + model_code)

        for i in range(len(RAW_PATHS)):
            # load jsonl path
            with open(RAW_PATHS[i], 'r') as jsonl_file:
                json_list = list(jsonl_file)
                json_list = [json.loads(x) for x in json_list]
            
            # instantiate model
            model = FinKBGenerator(model_name)

            # process relations
            finkb_list = model.extract_relations(json_list)
            custom_proc_path = PROC_PATHS[i].replace("finkb", model_code)
            utils.save_json(custom_proc_path, finkb_list)

            # extract dockey sentences
            sent_dict = model.extract_sentences(json_list)
            custom_sent_path = SENT_PATHS[i].replace("finkb", model_code)
            with open(custom_sent_path, 'w') as outfile:
                json.dump(sent_dict, outfile)


