# RELATION_METRICS
from f1 import compute_f1, safe_div
from mechanic_metric import span_metric
from sklearn import metrics
import numpy as np

def contains(span, gold_span, max_token_diff):
    '''
    Checks if span1 contains span2, with a max token difference
    '''
    span_length_diff = (span[1] - span[0]) - (gold_span[1] - gold_span[0])
    if (gold_span[0] >= span[0]) and (gold_span[1] <= span[1]) and (span_length_diff <= max_token_diff):
        return True
    return False

def fuzzy_match(ix, label, gold_relations, max_token_diff=5, nodir=False, nolabel=False):
    '''
    Checks if ix is similar to gold_ix
    '''
    span1, span2 = ix[0], ix[1]
    for gold_ix, gold_relation in gold_relations.items():
        gold_span1, gold_span2 = gold_ix[0], gold_ix[1]
        span1_contains_gold1 = contains(span1, gold_span1, max_token_diff)
        span2_contains_gold2 = contains(span2, gold_span2, max_token_diff)
        span1_contains_gold2 = contains(span1, gold_span2, max_token_diff)
        span2_contains_gold1 = contains(span2, gold_span1, max_token_diff)
        if nolabel and nodir and ((span1_contains_gold1 and span2_contains_gold2) or (span1_contains_gold2 and span2_contains_gold1)):
            return True
        elif nolabel and (not nodir) and span1_contains_gold1 and span2_contains_gold2:
            return True
        elif (not nolabel) and (gold_relation == label) and (not nodir) and span1_contains_gold1 and span2_contains_gold2:
            return True
        elif (not nolabel) and (gold_relation == label) and nodir and ((span1_contains_gold1 and span2_contains_gold2) or (span1_contains_gold2 and span2_contains_gold1)):
            return True
    return False


def unpack_relations(relation_list, threshold=-1):
    '''
    Parameters:
        relation_list (list)   : abstract list containing sentence list of predicted relations
        threshold (int)        : minimum confidence of prediction to accept (required for AUC). if thres < 0, no threshold is checked.
    '''
    compressed_relation_list = [relation_list[i][j] for i in range(len(relation_list)) for j in range(len(relation_list[i]))]
    processed_relation_list = []

    for sent_relation_list in compressed_relation_list:
        sent_processed_relation_dict = {}
        for relation in sent_relation_list:
            if threshold < 0:
                # no threshold, add all relations
                span_1, span_2, label = (relation[0], relation[1]), (relation[2], relation[3]), relation[4]
                sent_processed_relation_dict[(span_1, span_2)] = label
            else: 
                # threshold
                span_1, span_2, label, prob = (relation[0], relation[1]), (relation[2], relation[3]), relation[4], relation[6]
                if (prob > threshold):  # if high enough confidence in prediction
                    sent_processed_relation_dict[(span_1, span_2)] = label
        processed_relation_list.append(sent_processed_relation_dict)
    return processed_relation_list

def unpack_tokens(relation_list):
    unique_tokens = set()
    for (span_1, span_2), label in relation_list.items():
        for i in range(span_1[0], span_1[1] + 1):
            unique_tokens.add(i)
        for i in range(span_2[0], span_2[1] + 1):
            unique_tokens.add(i)
    return unique_tokens

def span_match(ix, label, gold_relations, sent_tokens, metric="rouge", nodir=False, nolabel=False):
    # retrieve span1 and span2
    span1, span2 = sent_tokens[ix[0][0]:ix[0][1]+1], sent_tokens[ix[1][0]:ix[1][1]+1]
    span1, span2 = " ".join(span1), " ".join(span2)

    for gold_ix, gold_relation in gold_relations.items():
        # retrieve gold span1 and gold span2
        gold_span1, gold_span2 = sent_tokens[gold_ix[0][0]:gold_ix[0][1]+1], sent_tokens[gold_ix[1][0]:gold_ix[1][1]+1]
        gold_span1, gold_span2 = " ".join(gold_span1), " ".join(gold_span2)

        if span_metric(span1, gold_span1, metric) and span_metric(span2, gold_span2, metric):
            if nolabel:
                return True
            if label == gold_relation:
                return True
        
        if nodir and span_metric(span2, gold_span1, metric) and span_metric(span1, gold_span2, metric):
            if nolabel:
                return True
            if label == gold_relation:
                return True
    return False

def compute_span_true_positive(ix, label, sent_gold_relations, sent_tokens, metric, max_token_diff=5):
    ix_reverse = (ix[1], ix[0])
    

    # ExactRel: if span1, span2, labels are exactly the same
    if (metric == "ExactRel") and (ix in sent_gold_relations) and (sent_gold_relations[ix] == label):
        return True
    
    # ExactRelND: if both spans identified (in any order), labels are exactly the same
    if ((metric == "ExactRelND") and (ix in sent_gold_relations) and (sent_gold_relations[ix] == label)) \
        or ((metric == "ExactRelND") and (ix_reverse in sent_gold_relations) and (sent_gold_relations[ix_reverse] == label)):
        return True
    
    # FuzzyRel: span1 contains gold_span1 and span2 contains gold_span2 and relation == label
    if (metric == "FuzzyRel") and fuzzy_match(ix, label, sent_gold_relations, max_token_diff, nodir=False, nolabel=False):
        return True
    
    # FuzzyRelND: span1 contains gold_span1 and span2 contains gold_span2 and relation == label 
    # or span2 contains gold_span1 and span1 contains gold_span2 and relation == label
    if (metric == "FuzzyRelND") and fuzzy_match(ix, label, sent_gold_relations, max_token_diff, nodir=True, nolabel=False): 
        return True

    # RougeRel: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "RougeRel") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="rouge", nodir=False, nolabel=False):
        return True

    # RougeRelND: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "RougeRelND") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="rouge", nodir=True, nolabel=False):
        return True

    # JaccardRel: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "JaccardRel") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="jaccard", nodir=False, nolabel=False):
        return True

    # JaccardRelND: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "JaccardRelND") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="jaccard", nodir=True, nolabel=False):
        return True

    # ExactSpan: span1 == gold_span1 and span2 == gold_span2
    if (metric == "ExactSpan") and ix in sent_gold_relations:
        return True

    # ExactSpanND: (span1 == gold_span1 and span2 == gold_span2) or (span2 == gold_span1 and span1 == gold_span2)
    if (metric == "ExactSpanND") and ((ix in sent_gold_relations) or (ix_reverse in sent_gold_relations)):
        return True
    
    # FuzzySpan: span1 contains gold_span1 and span2 contains gold_span2
    if (metric == "FuzzySpan") and fuzzy_match(ix, label, sent_gold_relations, max_token_diff, nodir=False, nolabel=True):
        return True
    
    # FuzzySpanND: span1 contains gold_span1 and span2 contains gold_span2 OR
    # span2 contains gold_span1 and span1 contains gold_span2
    if (metric == "FuzzySpanND") and fuzzy_match(ix, label, sent_gold_relations, max_token_diff, nodir=True, nolabel=True):
        return True

    # RougeSpan: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "RougeSpan") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="rouge", nodir=False, nolabel=True):
        return True

    # RougeSpanND: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "RougeSpanND") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="rouge", nodir=True, nolabel=True):
        return True

    # JaccardSpan: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "JaccardSpan") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="jaccard", nodir=False, nolabel=True):
        return True

    # JaccardSpanND: rouge(span1, gold_span1) > 0.5 and rouge(span2, gold_span2) > 0.5 and relation  == label
    if (metric == "JaccardSpanND") and span_match(ix, label, sent_gold_relations, sent_tokens, metric="jaccard", nodir=True, nolabel=True):
        return True

    return False

def unpack_sentences(sentence_list):
    processed_token_list = []
    for abstract in sentence_list:
        # create token list
        tokens = [tok for sentence in abstract for tok in sentence]
        # duplicate token list based on length of abstract
        for i in range(len(abstract)):
            processed_token_list.append(tuple(tokens))
    return processed_token_list

class SpanRelationMetrics:
    """
    Computes precision, recall, and micro-averaged F1 from a list of predicted and gold spans.
    """
    def __init__(self):
        self.reset()

    def __call__(self, pred_relation_list, gold_relation_list, sentence_list, max_token_diff=5):
        # process relations
        processed_pred_relation_list = unpack_relations(pred_relation_list)
        processed_gold_relation_list = unpack_relations(gold_relation_list)
        processed_sentence_list = unpack_sentences(sentence_list)

        for sent_pred_relations, sent_gold_relations, sent_tokens in zip(processed_pred_relation_list, processed_gold_relation_list, processed_sentence_list):
            # update total gold and predicted 
            self._total_gold += len(sent_gold_relations)
            self._total_predicted += len(sent_pred_relations)

            # span-based metrics
            for ix, label in sent_pred_relations.items():
                for metric in self._span_metrics:
                    tp = compute_span_true_positive(ix, label, sent_gold_relations, sent_tokens, metric, max_token_diff=max_token_diff)
                    if tp:
                        self._true_positive[metric] += 1


    def get_metric(self, reset=False):
        computed_metrics = {}
        # retrieve span metrics
        for span_metric in self._span_metrics:
            
            total_gold, total_pred = self._total_gold, self._total_predicted
            true_positive = self._true_positive[span_metric]
            precision, recall, f1 = compute_f1(total_pred, total_gold, true_positive)
            computed_metrics[span_metric] = {"precision": precision, "recall": recall, "f1": f1}

        if reset:
            self.reset()
        
        return computed_metrics

    def reset(self):
        self._span_metrics = [
            "ExactRel", "ExactRelND", "FuzzyRel", "FuzzyRelND", \
            "RougeRel", "RougeRelND", "JaccardRel", "JaccardRelND", \
            "ExactSpan", "ExactSpanND", "FuzzySpan", "FuzzySpanND", \
            "RougeSpan", "RougeSpanND", "JaccardSpan", "JaccardSpanND"]
        self._total_gold = 0
        self._total_predicted = 0
        self._true_positive = {x:0 for x in self._span_metrics}


class TokenRelationMetrics:
    """
    Computes precision, recall, and micro-averaged F1 from a list of predicted and gold spans.
    """
    def __init__(self, prob=False):
        self.reset()
        self._prob = prob

    def __call__(self, pred_relation_list, gold_relation_list, sentence_list):
        # process sentence
        processed_sentence_list = [len(sentence) for abstract in sentence_list for sentence in abstract]
        total_tokens = sum(processed_sentence_list)

        # prepare precision, recall, f1 requirements
        total_gold, total_pred, true_pos, tpr, fpr = self.compute_metric_values(pred_relation_list, gold_relation_list, total_tokens)

        self._total_gold = total_gold
        self._total_predicted = total_pred
        self._true_positive = true_pos

        # prepare auc requirements
        if self._prob:
            max_divisible = 100
            for i in range(0, max_divisible + 1):
                threshold = i / max_divisible
                _, _, _, tpr, fpr = self.compute_metric_values(pred_relation_list, gold_relation_list, total_tokens, threshold=threshold)
                self._tpr_list.append(tpr)
                self._fpr_list.append(fpr)
        
        
    def compute_metric_values(self, pred_relation_list, gold_relation_list, total_tokens, threshold=-1):
        processed_pred_relation_list = unpack_relations(pred_relation_list, threshold=threshold)
        processed_gold_relation_list = unpack_relations(gold_relation_list)

        total_gold_pos, total_pred_pos, true_pos = 0, 0, 0
        for sent_pred_relations, sent_gold_relations in zip(processed_pred_relation_list, processed_gold_relation_list):
            sent_gold_tokens = unpack_tokens(sent_gold_relations)
            sent_pred_tokens = unpack_tokens(sent_pred_relations)
            total_gold_pos += len(sent_gold_tokens)
            total_pred_pos += len(sent_pred_tokens)
            
            for pred_token in sent_pred_tokens:
                if pred_token in sent_gold_tokens:
                    true_pos += 1
        
        false_pos = total_pred_pos - true_pos
        total_gold_neg = total_tokens - total_gold_pos 
        tpr = safe_div(true_pos, total_gold_pos)
        fpr = safe_div(false_pos, total_gold_neg)

        return total_gold_pos, total_pred_pos, true_pos, tpr, fpr

    def get_metric(self, reset=False):
        precision, recall, f1 = compute_f1(self._total_predicted, self._total_gold, self._true_positive)
        computed_metrics = {"precision": precision, "recall": recall, "f1":f1}

        if self._prob:
            auc = metrics.auc(np.array(self._fpr_list), np.array(self._tpr_list))
            computed_metrics["auc"] = auc

        if reset:
            self.reset()
        
        return {"Token": computed_metrics}

    def reset(self):
        self._total_gold = 0
        self._total_predicted = 0
        self._true_positive = 0
        self._tpr_list = []
        self._fpr_list = []
