import spacy
import nltk
from nltk.tag.stanford import StanfordNERTagger
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import pandas as pd
from rouge_score import rouge_scorer

def load_jsonl(file_path):
    raw_data = []
    with open(file_path, "r") as f:
        for line in f:
            # read line
            json_line = json.loads(line)
            raw_data.append(json_line)
    return raw_data

def exact_match(span1, span2):
    return span1.strip().lower() == span2.strip().lower()

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return len(s1.intersection(s2)) / len(s1.union(s2))

def span_metric(span1, span2, metric):
    if metric =="substring":
        return ((span1 in span2) or (span2 in span1))
    elif metric =="jaccard":
        j = jaccard_similarity(span1.split(),span2.split())
        return (j > 0.5)
    elif metric =="rouge":
        scorer = rouge_scorer.RougeScorer(['rouge1'])
        scores = scorer.score(span1, span2)
        return (scores['rouge1'].fmeasure > 0.5)
    elif metric == "exact":
        return exact_match(span1, span2)
    return False

def generate_spacy_prediction(abstract_text):
    doc = nlp_spacy(abstract_text)
    spacy_entities = []
    for ent in doc.ents:
        ent_start, ent_end = ent.start, ent.end - 1
        spacy_entities.append([ent_start, ent_end, 'ENTITY'])
    return spacy_entities

def generate_bertner_prediction(abstract_text):
    doc = nlp_bertbasedner(abstract_text)
    bertner_entities = []
    for ent in doc:
        ent_text = ent["word"].split(" ")
        try:
            ent_start = abstract_sents.index(ent_text[0])
            ent_end = abstract_sents.index(ent_text[-1])
            bertner_entities.append([ent_start, ent_end, 'ENTITY'])
        except:
            continue
    return bertner_entities

def generate_nltk_prediction(abstract_text):
    ne_tree = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(abstract_text)))
    index = 0
    nltk_entities = []
    for chunk in ne_tree:
        if hasattr(chunk, 'label'):
            nltk_entities.append([index, index+len(chunk)-1, 'ENTITY'])
            index += len(chunk)
        else:
            index += 1
    return nltk_entities

def generate_stanford_prediction(abstract_text):
    doc = nlp_stanford.tag(nltk.word_tokenize(abstract_text))
    stanford_entities = []
    curr_tag, curr_entity = 'O', []
    for i in range(len(doc)):
        word, label = doc[i]
        if (label != 'O') and ((curr_tag == 'O') or (curr_tag == label)):
            curr_entity.append(i)
            curr_tag = label
        elif (label != 'O') and (curr_tag != label):
            stanford_entities.append([min(curr_entity), max(curr_entity), 'ENTITY'])
            curr_entity = [i, ]
            curr_tag = label
        elif (label == 'O') and (curr_tag != 'O'):
            stanford_entities.append([min(curr_entity), max(curr_entity), 'ENTITY'])
            curr_tag, curr_entity = 'O', []
        else:
            continue
    return stanford_entities

if __name__ == "__main__":
    # load nlp model
    nlp_spacy = spacy.load("en_core_web_sm")

    # load tokenizer
    tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    nlp_bertbasedner = pipeline("ner", model=model, tokenizer=tokenizer)

    # path to stanford model
    PATH_TO_JAR = 'models/stanford-ner/stanford-ner.jar'
    PATH_TO_MODEL = 'models/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'
    nlp_stanford = StanfordNERTagger(model_filename=PATH_TO_MODEL,path_to_jar=PATH_TO_JAR, encoding='utf-8')

    data = load_jsonl("data/predictions/dyfinie/finmechanic/coarse/test.jsonl")
    scores = {
        (model, metric): { 'tp': 0, 'fp': 0, 'fn': 0 } for metric in ['jaccard', 'rouge', 'substring', 'exact'] 
        for model in ['spacy', 'bert', 'nltk', 'stanford', 'dyfinie']
    }

    for abstract in data:
        abstract_sents = sum(abstract["sentences"], [])
        abstract_text = " ".join(abstract_sents)
        
        # generate gold ner
        gold_ner = sum(abstract["ner"], [])
        
        # generate predicted ner
        pred_ner_spacy = generate_spacy_prediction(abstract_text)
        pred_ner_bert = generate_bertner_prediction(abstract_text)
        pred_ner_nltk = generate_nltk_prediction(abstract_text)
        pred_ner_stanford = generate_stanford_prediction(abstract_text)
        pred_ner_dyfinie = sum(abstract["predicted_ner"], [])
        
        preds = {
            'spacy': pred_ner_spacy, 
            'bert': pred_ner_bert,
            'nltk': pred_ner_nltk,
            'stanford': pred_ner_stanford,
            'dyfinie': pred_ner_dyfinie
        }
        
        # compare gold ner and predicted ner and compare similarity
        # tp = corr ent, fp = pred ent but not gold, fn = gold ent but not pred
        identified = {
            model: { metric: [False] * len(gold_ner) for metric in ['jaccard', 'rouge', 'substring', 'exact']  } 
            for model in ['spacy', 'bert', 'nltk', 'stanford', 'dyfinie']
        }
        for model in preds.keys():
            for metric in ['jaccard', 'rouge', 'substring', 'exact']:
                for pred_ent in preds[model]:
                    for gold_ent_id in range(len(gold_ner)):
                        gold_ent = gold_ner[gold_ent_id]
                        corr_ent = False

                        pred_ent_str = " ".join(abstract_sents[pred_ent[0]:pred_ent[1]+1])
                        gold_ent_str = " ".join(abstract_sents[gold_ent[0]:gold_ent[1]+1])

                        # compute metric
                        metric_score = span_metric(pred_ent_str, gold_ent_str, metric)

                        if metric_score:
                            corr_ent = True
                            identified[model][metric][gold_ent_id] = True
                            
                    # update entity as correct or wrong
                    if corr_ent:
                        scores[(model, metric)]['tp'] += 1
                    else:
                        scores[(model, metric)]['fp'] += 1

                # update false negatives
                scores[(model, metric)]['fn'] = sum([x == False for x in identified[model][metric]])

    df = pd.DataFrame(scores)
    df.to_csv("data/evaluations/ner_model_scores.csv")
