import encoder
import os 
import sys
# set working directory
sys.path.append(os.getcwd())
import utils

# Load finbert model
models = {
    'stsb_multiqa': encoder.Encoder('models/stsb-multi-qa-MiniLM-L6-cos-v1'),
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5'),
    'roberta': encoder.Encoder('stsb-roberta-large'),
    'fin_multiqa': encoder.Encoder('models/fin-multiqa'),
    'fin_msmarco': encoder.Encoder('models/fin-msmarco')
}
# EVALUATION RESULTS:
# {'stsb_multiqa': 0.44779870183517534, 'finbert': 0.16960061550140382, 'multiqa': 0.465436761106054, 
# 'msmarco': 0.4332077649856607, 'roberta': 0.3410490820556879, 'fin_multiqa': 0.48745486815770467, 
# 'fin_msmarco': 0.44320187172542014, 'fin_tapt':0.24985654120643934}

def compute_similarity(e1, e2, model):
    e1_embedding = models[model].encode_entity(e1.strip())
    e2_embedding = models[model].encode_entity(e2.strip())
    rel_score = models[model].entity_similarity(e1_embedding, e2_embedding)
    return rel_score

def compute_relation_ratio(e1, e2, e3, model):
    e1_embedding = models[model].encode_entity(e1.strip())
    e2_embedding = models[model].encode_entity(e2.strip())
    e3_embedding = models[model].encode_entity(e3.strip())

    rel12 = models[model].entity_similarity(e1_embedding, e2_embedding)
    rel13 = models[model].entity_similarity(e1_embedding, e3_embedding)

    return (rel12 - rel13)

def compute_relation_diff(e1, e2, e3, model):
    e1_embedding = models[model].encode_entity(e1.strip())
    e2_embedding = models[model].encode_entity(e2.strip())
    e3_embedding = models[model].encode_entity(e3.strip())

    rel12 = models[model].entity_similarity(e1_embedding, e2_embedding)
    rel13 = models[model].entity_similarity(e1_embedding, e3_embedding)

    return int(rel12 > rel13)

if __name__ == "__main__":
    # load relational test data
    relational_data = utils.load_json("data/finsearch/test.json")

    # store average scores
    avg_scores = {}
    odr_scores = {}
    odr_scores_perc = {}

    for model_name in models.keys():
        # compute relation scores
        scores = [compute_relation_ratio(row["sent_a"], row["sent_b"], row["sent_c"], model_name) for row in relational_data]
        score_counts = [compute_relation_diff(row["sent_a"], row["sent_b"], row["sent_c"], model_name) for row in relational_data]
        
        # update average scores
        avg_scores[model_name] = sum(scores) / len(scores)
        odr_scores[model_name] = sum(score_counts)
        odr_scores_perc[model_name] = sum(score_counts) / len(relational_data)


    print("AVERAGE SCORES:", avg_scores)
    print("ORDERED SCORES:", odr_scores)
    print("ORDERED SCORES PERC:", odr_scores_perc)