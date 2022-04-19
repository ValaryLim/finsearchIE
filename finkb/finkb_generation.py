# this file is ot generate finkb 
import json
import encoder

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

def extract_relations(json_list):
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
                    "E1_CODE": encoder.encode_entity(e1_str),
                    "E2_CODE": encoder.encode_entity(e2_str),
                    "E1_START": e1_start, 
                    "E1_END": e1_end, 
                    "E2_START": e2_start, 
                    "E2_END": e2_end, 
                    "REL": r,
                    "DOC_KEY": abstract["doc_key"]
                })

    return extracted_rels

def extract_sentences(json_list):
    sentence_dict = {}
    for abstract in json_list:
        # combine sentences
        combined_sentences = sum(abstract["sentences"], [])
        # update sentence dict
        sentence_dict[abstract["doc_key"]] = combined_sentences
    return sentence_dict

def save_json(file_path, abstract_list):
    with open(file_path, "w") as f:
        for abstract in abstract_list:
            print(json.dumps(abstract), file=f)

if __name__ == "__main__":
    for i in range(len(RAW_PATHS)):
        # load jsonl path
        with open(RAW_PATHS[i], 'r') as jsonl_file:
            json_list = list(jsonl_file)
            json_list = [json.loads(x) for x in json_list]

        # process relations 
        finkb_list = extract_relations(json_list) 
        save_json(PROC_PATHS[i], finkb_list)

        # extract dockey sentences
        sent_dict = extract_sentences(json_list)
        with open(SENT_PATHS[i], 'w') as outfile:
            json.dump(sent_dict, outfile)