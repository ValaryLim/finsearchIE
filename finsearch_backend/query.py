import utils
import encoder
import abstract

# Load finbert model
models = {
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5'),
    'roberta': encoder.Encoder('stsb-roberta-large')
}

# Load FinKB entities
finkbs = {
    'finbert': {
        'granular': utils.load_jsonl('data/finkb/finbert/granular.jsonl'),
        'coarse': utils.load_jsonl('data/finkb/finbert/coarse.jsonl')
    },
    'multiqa': {
        'granular': utils.load_jsonl('data/finkb/multiqa/granular.jsonl'),
        'coarse': utils.load_jsonl('data/finkb/multiqa/coarse.jsonl')
    },
    'msmarco': {
        'granular': utils.load_jsonl('data/finkb/msmarco/granular.jsonl'),
        'coarse': utils.load_jsonl('data/finkb/msmarco/coarse.jsonl')
    },
    'roberta': {
        'granular': 'none',
        'coarse': 'none'
        # 'granular': utils.load_jsonl('data/finkb/roberta/finance_granular_coref_sample.jsonl'),
        # 'coarse': utils.load_jsonl('data/finkb/roberta/finance_coarse_coref_sample.jsonl')
    },
}

def search_query(e1, e2, granular=True, dir=False, threshold=0.5, top=100, model="finbert"):
    e1_embedding = models[model].encode_entity(e1.strip())
    e2_embedding = models[model].encode_entity(e2.strip())

    # select finkb
    granular_str = "granular" if granular else "coarse"
    finkb_list = finkbs[model][granular_str]
    
    similar_abstracts_dict = { }
    # iterate thru all finkb entities
    for rel in finkb_list:
        # query similarity
        rel_score = models[model].query_similarity(e1_embedding, e2_embedding, rel["E1_CODE"], rel["E2_CODE"], dir)

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
    similar_abstracts_list = sorted(similar_abstracts_dict.values(), reverse=True)[:top]

    # retrieve jsons
    similar_abstracts_dict = {
        x.get_doc_key() : x.to_dict() for x in similar_abstracts_list
    }

    return similar_abstracts_dict
