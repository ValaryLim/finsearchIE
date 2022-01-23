from finbert_embedding.embedding import FinbertEmbedding
from scipy import spatial

# load finbert model
finbert = FinbertEmbedding()

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