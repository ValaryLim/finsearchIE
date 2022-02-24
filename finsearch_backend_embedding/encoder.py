from sentence_transformers import SentenceTransformer, util
import torch
from finbert_embedding.embedding import FinbertEmbedding

class Encoder: 
    def __init__(self, model_name):
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
    
    def query_similarity(self, query1, query2, gold1, gold2, dir=False):
        sim11 = self.entity_similarity(query1, gold1)
        sim12 = self.entity_similarity(query1, gold2)
        sim21 = self.entity_similarity(query2, gold1)
        sim22 = self.entity_similarity(query2, gold2)

        if dir: # direction of entity matters
            return (sim11 + sim22)/2
        else:
            return max((sim11 + sim22)/2, (sim12 + sim21)/2)