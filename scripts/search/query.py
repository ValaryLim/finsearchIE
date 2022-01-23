import abstract
import encoder 
import json

# load finkb entities
FINKB_GRANULAR_PATH = "data/finkb/finance_granular_coref_sample.jsonl"
FINKB_COARSE_PATH = "data/finkb/finance_coarse_coref.jsonl"

with open(FINKB_GRANULAR_PATH, 'r') as jsonl_file:
    FINKB_GRANULAR = list(jsonl_file)
    FINKB_GRANULAR = [json.loads(x) for x in FINKB_GRANULAR][:50]

FINKB_COARSE = None 

def query(e1, e2, granular=True, dir=False, threshold=0.5, top=100):
    e1_embedding = encoder.encode_entity(e1)
    e2_embedding = encoder.encode_entity(e2)

    # select finkb
    if granular:
        finkb_list = FINKB_GRANULAR
    else:
        finkb_list = FINKB_COARSE
    
    similar_abstracts_dict = { }
    # iterate thru all finkb entities
    for rel in finkb_list:
        # query similarity
        rel_score = encoder.query_similarity(e1_embedding, e2_embedding, rel["E1_CODE"], rel["E2_CODE"], dir)
        doc_key = rel["DOC_KEY"]
        # update similarity document
        if rel_score > threshold:
            if doc_key in similar_abstracts_dict:
                similar_abstracts_dict[doc_key].add_relation(rel, rel_score)
            else:
                new_abstract = abstract.Abstract(doc_key)
                new_abstract.add_relation(rel, rel_score)
                similar_abstracts_dict[doc_key] = new_abstract
    
    # select top abstracts
    similar_abstracts_list = sorted(similar_abstracts_dict.values(), reverse=True)

    for abst in similar_abstracts_list:
        print(abst.doc_key, abst.relation_score)
    return similar_abstracts_list

print(query("economic growth", "money"))