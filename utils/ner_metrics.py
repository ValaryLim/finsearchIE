from rouge_score import rouge_scorer
scorer = rouge_scorer.RougeScorer(['rouge1'])


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
        scores = scorer.score(span1, span2)
        return (scores['rouge1'].fmeasure > 0.5)
    elif metric == "exact":
        return exact_match(span1, span2)
    return False