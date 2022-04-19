import encoder
import utils

# LOAD MODELS 
# MODIFY THIS LIST IF YOU WISH TO COMPARE OTHER MODELS
models = {
    'stsb_multiqa': encoder.Encoder('models/stsb-multi-qa-MiniLM-L6-cos-v1'),
    'finbert': encoder.Encoder('ProsusAI/finbert'),
    'multiqa': encoder.Encoder('multi-qa-MiniLM-L6-cos-v1'),
    'msmarco': encoder.Encoder('msmarco-MiniLM-L6-cos-v5'),
    'roberta': encoder.Encoder('stsb-roberta-large'),
    'fin_multiqa': encoder.Encoder('../finsearch_embedder/models/finmultiqa'),
    'fin_msmarco': encoder.Encoder('../finsearch_embedder/models/finmsmarco')
}

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
    relational_data = utils.load_json("finsemantic/test.json")

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