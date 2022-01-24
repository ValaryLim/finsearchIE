import utils
import abstract
from finbert_embedding.embedding import FinbertEmbedding
from scipy import spatial

# Load finbert model
finbert = FinbertEmbedding()

# Load FinKB entities
# FINKB_COARSE = utils.load_jsonl("data/finance_coarse_coref.jsonl")
FINKB_GRANULAR = utils.load_jsonl("data/finance_granular_coref_sample.jsonl")

print("all loaded")

def encode_entity(text):
    return finbert.sentence_vector(text).tolist()

def entity_similarity(embedding1, embedding2):
    return (1 - spatial.distance.cosine(embedding1, embedding2))

def query_similarity(query1, query2, gold1, gold2, dir = False):
    sim11 = entity_similarity(query1, gold1)
    sim12 = entity_similarity(query1, gold2)
    sim21 = entity_similarity(query2, gold1)
    sim22 = entity_similarity(query2, gold2)

    if dir: # direction of entity matters
        return max(sim11, sim22)
    else: # ignore direction
        return max(sim11, sim12, sim21, sim22) 

def clean_entity(text):
    return text.strip().lower()

def search_query(e1, e2, granular=True, dir=False, threshold=0.5, top=100):
    e1_embedding = encode_entity(clean_entity(e1))
    e2_embedding = encode_entity(clean_entity(e2))

    # select finkb
    if granular:
        finkb_list = FINKB_GRANULAR
    else:
        finkb_list = FINKB_COARSE
    
    similar_abstracts_dict = { }
    # iterate thru all finkb entities
    for rel in finkb_list:
        # query similarity
        rel_score = query_similarity(e1_embedding, e2_embedding, rel["E1_CODE"], rel["E2_CODE"], dir)
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
