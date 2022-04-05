'''
Finsearch Backend Embedding Main Application Start-Up Page
'''
print("Starting Up Finsearch Backend Embedder Microservice...")

# INSTALLED PACKAGES
from flask import Flask, request
import numpy as np

# FINSEARCH BACKEND EMBEDDER PACKAGES
import utils
import abstract
import encoder
import search_model

print("Packages Loaded. Loading Models and Data...")

# EMBEDDERS
models = {
    'finmultiqa': encoder.Encoder('models/finmultiqa'),
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5')
}

# RELATIONAL TRIPLET DATA
relation_info = {
    'finbert': {
        'granular': utils.load_jsonl('data/finbert/granular_info.jsonl'),
        'coarse': utils.load_jsonl('data/finbert/coarse_info.jsonl')
    },
    'multiqa': {
        'granular': utils.load_jsonl('data/multiqa/granular_info.jsonl'),
        'coarse': utils.load_jsonl('data/multiqa/coarse_info.jsonl')
    },
    'msmarco': {
        'granular': utils.load_jsonl('data/msmarco/granular_info.jsonl'),
        'coarse': utils.load_jsonl('data/msmarco/coarse_info.jsonl')
    },
    'finmultiqa': {
        'granular': utils.load_jsonl('data/finmultiqa/granular_info.jsonl'),
        'coarse': utils.load_jsonl('data/finmultiqa/coarse_info.jsonl')
    }
}

# NNDESCENT GRAPHS
relation_train = {
    'finbert': {
        'granular': {
            True: search_model.generate_index('data/finbert/granular_train.npy', True),
            False: search_model.generate_index('data/finbert/granular_train.npy', False),
        }, 
        'coarse': {
            True: search_model.generate_index('data/finbert/coarse_train.npy', True),
            False: search_model.generate_index('data/finbert/coarse_train.npy', False),
        }
    },
    'multiqa': {
        'granular': {
            True: search_model.generate_index('data/multiqa/granular_train.npy', True),
            False: search_model.generate_index('data/multiqa/granular_train.npy', False),
        }, 
        'coarse': {
            True: search_model.generate_index('data/multiqa/coarse_train.npy', True),
            False: search_model.generate_index('data/multiqa/coarse_train.npy', False),
        }
    },
    'msmarco': {
        'granular': {
            True: search_model.generate_index('data/msmarco/granular_train.npy', True),
            False: search_model.generate_index('data/msmarco/granular_train.npy', False),
        }, 
        'coarse': {
            True: search_model.generate_index('data/msmarco/coarse_train.npy', True),
            False: search_model.generate_index('data/msmarco/coarse_train.npy', False),
        }
    },
    'finmultiqa': {
        'granular': {
            True: search_model.generate_index('data/finmultiqa/granular_train.npy', True),
            False: search_model.generate_index('data/finmultiqa/granular_train.npy', False),
        }, 
        'coarse': {
            True: search_model.generate_index('data/finmultiqa/coarse_train.npy', True),
            False: search_model.generate_index('data/finmultiqa/coarse_train.npy', False),
        }
    }
}

print("FINSEARCH BACKEND LOADED...")

# Instantiate the Application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def main():
    '''
    Route to check if Microservice is alive.
    '''
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
    embedding = np.array(list(e1_embedding) + list(e2_embedding))

    # select data
    granular_str = "granular" if granular else "coarse"
    relevant_relation_info = relation_info[model][granular_str]
    relevant_search_index = relation_train[model][granular_str][direction]

    # retrieve top relations
    neighbours = relevant_search_index.query(
        np.array([embedding,]), top * 10
    )
    relation_index, relation_score = neighbours[0][0], neighbours[1][0]

    # extract relevant abstracts
    similar_abstracts_dict = {}
    for ind in range(len(relation_score)):
        rel_ind = relation_index[ind]
        rel_score = relation_score[ind]
        rel_score = 1-np.exp2(rel_score)
        rel_info = relevant_relation_info[rel_ind]
        doc_key = rel_info["DOC_KEY"]

        # update similarity document
        if rel_score > threshold:
            if doc_key in similar_abstracts_dict:
                similar_abstracts_dict[doc_key].add_relation(rel_info, rel_score)
            else:
                new_abstract = abstract.Abstract(doc_key)
                new_abstract.add_relation(rel_info, rel_score)
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
    '''
    This route:
    1. Retrieves requested arguments
    2. Runs search query
    3. Returns query results as json
    '''
    # retrieve request arguments
    entity1 = request.args.get('entity1')
    entity2 = request.args.get('entity2')
    direction = bool(request.args.get('direction'))
    threshold = float(request.args.get('threshold'))
    granular = bool(request.args.get('granular'))
    model = request.args.get('model')

    print(f"Search Query Called: \
        {entity1} {entity2} {threshold} {direction} {granular} {model}")
    
    # retrieve search query results
    results = search_query(
        e1=entity1, e2=entity2, 
        granular=granular, direction=direction, threshold=threshold, 
        model=model
    )
    print("Search Results Returned.")

    # return results
    return {
        0: results
        }

if __name__ == "__main__":
    app.run(port=5000)
