from sentence_transformers import SentenceTransformer, util
from numba import jit
import numpy as np
import torch
from finbert_embedding.embedding import FinbertEmbedding

@jit
def _entity_similarity(x, y):
    norm_x, norm_y, result = 0.0, 0.0, 0.0
    dim = x.shape[0]
    for i in range(dim):
        result += x[i] * y[i]
        norm_x += x[i] * x[i]
        norm_y += y[i] * y[i]
    cosine = (result / np.sqrt(norm_x * norm_y))
    return cosine


class Encoder: 
    def __init__(self, model_name):
        print("Loading model...", model_name)
        self.model_name = model_name
        if "finbert" in self.model_name:
            self.model = FinbertEmbedding()
        else:
            self.model = SentenceTransformer(self.model_name)
        
    def encode_entity(self, text):
        if "finbert" in self.model_name:
            return self.model.sentence_vector(text).tolist()
        else:
            return self.model.encode(text, convert_to_tensor=True).tolist()
    
    def entity_similarity(self, embedding1, embedding2):
        embedding1 = torch.Tensor(embedding1)
        embedding2 = torch.Tensor(embedding2)
        rel_score = util.pytorch_cos_sim(embedding1, embedding2)
        return float(rel_score[0][0])

    def entity_similarity_numba(self, embedding1, embedding2):
        rel_score = _entity_similarity(embedding1, embedding2)
        return float(rel_score)

    def query_similarity(self, query1, query2, dir, gold):
        gold1, gold2 = gold["E1_CODE"], gold["E2_CODE"]
        sim11 = self.entity_similarity(query1, gold1)
        sim12 = self.entity_similarity(query1, gold2)
        sim21 = self.entity_similarity(query2, gold1)
        sim22 = self.entity_similarity(query2, gold2)

        if dir: # direction of entity matters
            return (sim11 + sim22)/2
        else:
            return max((sim11 + sim22)/2, (sim12 + sim21)/2)
    
    def query_similarity_numba(self, query1, query2, dir, gold):
        # convert to numpy array
        gold1, gold2 = np.array(gold["E1_CODE"]), np.array(gold["E2_CODE"])
        query1, query2 = np.array(query1), np.array(query2)
        # compute similarity score using numba
        sim11 = self.entity_similarity_numba(query1, gold1)
        sim12 = self.entity_similarity_numba(query1, gold2)
        sim21 = self.entity_similarity_numba(query2, gold1)
        sim22 = self.entity_similarity_numba(query2, gold2)
        # return score
        if dir: # direction of entity matters
            return (sim11 + sim22)/2
        else:
            return max((sim11 + sim22)/2, (sim12 + sim21)/2)
