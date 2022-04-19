'''
DEPRECATED APPLICATION (NAIVE SEARCH ALGORITHM)

This Python file contains the deprecated code that runs the search for related
abstracts using the Naive Search Algorithm with Parallel Processing and Numba
compilation.

We have since moved the app functionalities to app.py, and are no longer using
this file. This file is kept solely for documentation purposes. 
'''
from flask import Flask, request
import multiprocessing
import utils
import encoder
import abstract
import functools
import logging

# EMBEDDERS
models = {
    'finmultiqa': encoder.Encoder('models/finmultiqa'),
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5')
}

# FINKB
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

logging.info("FINSEARCH BACKEND LOADED...")
print("FINSEARCH BACKEND LOADED...")

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS

@app.route("/")
def main():
    return "<h1>Finsearch Backend Embedder Microservice</h1>"

def search_query(
    e1, e2, 
    granular=True, direction=False, threshold=0.5, top=100, model="finbert"
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

    # compute relation scores
    global relation_scores
    with multiprocessing.Pool(processes=20) as pool:
        func = functools.partial(
            selected.query_similarity_numba, e1_embedding, e2_embedding, dir)
        relation_scores = pool.map(func, finkb_list)
        # func = functools.partial(
        #     selected.query_similarity, e1_embedding, e2_embedding, dir)
        # relation_scores = pool.map(func, finkb_list)

    # extract relevant abstracts
    similar_abstracts_dict = {}
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

    return top_abstracts_dict

@app.route("/search")
def search():
    # retrieve request arguments
    entity1 = request.args.get('entity1')
    entity2 = request.args.get('entity2')
    direction = bool(request.args.get('direction'))
    threshold = float(request.args.get('threshold'))
    granular = bool(request.args.get('granular'))
    model = request.args.get('model')

    logging.info(f"Search Query Called: \
        {entity1} {entity2} {threshold} {direction} {granular} {model}")
    
    # retrieve search query results
    results = search_query(
        e1=entity1, e2=entity2, 
        granular=granular, direction=direction, threshold=threshold, 
        model=model
    )

    logging.info("Search Results Returned.")

    return {
        0: results
        }

if __name__ == "__main__":
    app.run(port=5000)
