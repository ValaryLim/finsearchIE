import json

with open("data/finkb/finance_granular_sents.json", 'r') as json_file:
    FINKB_GRANULAR_SENTS = json.load(json_file)

class Relation:
    def __init__(self, relation_dict, relation_score):
        self.e1_str = relation_dict["E1"]
        self.e1_start = relation_dict["E1_START"]
        self.e1_end = relation_dict["E1_END"]
        self.e2_str = relation_dict["E2"]
        self.e2_start = relation_dict["E2_START"]
        self.e2_end = relation_dict["E2_END"]
        self.relation = relation_dict["REL"]
        self.relation_score = relation_score

    def get_relation_span(self):
        relation_start = min(self.e1_start, self.e2_start)
        relation_end = max(self.e1_end, self.e2_end)
        return [relation_start, relation_end]
    
    def get_relation_score(self):
        return self.relation_score

class Abstract:
    def __init__(self, doc_key):
        self.doc_key = doc_key 
        self.relation_score = -1
        self.relations = []
        self.abstract = FINKB_GRANULAR_SENTS[str(self.doc_key)]
    
    def get_relation_score(self):
        return self.relation_score

    def update_relation_score(self, relation):
        self.relation_score = max(self.relation_score, relation.get_relation_score())
    
    def add_relation(self, new_relation, new_relation_score):
        # create new relation
        new_relation_obj = Relation(new_relation, new_relation_score)

        # update relation score
        self.update_relation_score(new_relation_obj)

        # add relation
        self.relations.append(new_relation_obj)

    def __lt__(self, other):
        return self.get_relation_score() < other.get_relation_score()
    

