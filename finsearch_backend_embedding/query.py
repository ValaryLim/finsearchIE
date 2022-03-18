'''
LEGACY CODE. NO LONGER BEING USED.
'''
import utils
import encoder
import abstract
import multiprocessing

# Load finbert model
models = {
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'finmultiqa': encoder.Encoder('models/finmultiqa'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5')
}


# Load FinKB entities
finkbs = {
    'finbert': {
        'granular': utils.load_jsonl('data/finbert/granular.jsonl'),
        'coarse': utils.load_jsonl('data/finbert/coarse.jsonl')
    },
    'multiqa': {
        'granular': utils.load_jsonl('data/multiqa/granular.jsonl'),
        'coarse': utils.load_jsonl('data/multiqa/coarse.jsonl')
    },
    'msmarco': {
        'granular': utils.load_jsonl('data/msmarco/granular.jsonl'),
        'coarse': utils.load_jsonl('data/msmarco/coarse.jsonl')
    },
    'finmultiqa': {
        'granular': utils.load_jsonl('data/finmultiqa/granular.jsonl'),
        'coarse': utils.load_jsonl('data/finmultiqa/coarse.jsonl')
    }
}


def search_query(
    e1, e2, granular=True, direction=False, threshold=0.5, 
    top=100, model="finbert"
):
    '''
    Query function that embeds searched entities, accepts search parameters, 
    and returns list of query results. 

    Parameters:
    e1 (string)         : query entity 1
    e2 (string)         : query entity 2
    granular (bool)     : if true, will return granular relations
                          else, return coarse relations
    direction (bool)    : if true, will only check if query1 == gold1 and 
                          query2 == gold2.
                          else, check if (query1 == gold1 and query2 == gold2) 
                          or (query1 == gold2 and query2 == gold1)
    threshold (float)   : only returns abstracts with a relation score greater 
                          than threshold
    top (int)           : returns the top number of queries by relation score, 
                          or all relevant abstracts (if lower than top)
    model (string)      : search model to use
    '''
    selected = models[model]
    e1_embedding = selected.encode_entity(e1.strip())
    e2_embedding = selected.encode_entity(e2.strip())

    # select finkb
    granular_str = "granular" if granular else "coarse"
    finkb_list = finkbs[model][granular_str]

    similar_abstracts_dict = {}
    with multiprocessing.Manager() as manager:
        relation_scores = manager.list(range(len(finkb_list)))
        
        processes = []
        for ind in range(len(finkb_list)):
            rel = finkb_list[ind]
            arguments = (e1_embedding, e2_embedding, rel["E1_CODE"], \
                rel["E2_CODE"], direction, ind, relation_scores)
            p = multiprocessing.Process(
                target=selected.query_similarity, args=arguments)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        for ind in range(len(finkb_list)):
            rel, rel_score = finkb_list[ind], relation_scores[ind]
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
    top_abstracts = sorted(similar_abstracts_dict.values(), reverse=True)[:top]

    # retrieve jsons
    top_abstracts_dict = {
        x.get_doc_key() : x.to_dict() for x in top_abstracts
    }

    # return similar_abstracts_dict
    return top_abstracts_dict
