# Relation and Abstract classes
# Loads additional abstract information using doc_key for Abstract
import utils

# Load abstract sentences information
FINKB_SENTENCES = utils.load_json("data/abstract_sentences.json")
FINKB_EXTRAINFO = utils.load_csv("data/abstract_extra_info.csv", list_cols = ['authors'])

print("loaded")

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

    def to_dict(self):
        relation_dict = {
            'e1': self.e1_str, 
            'e1_start': self.e1_start, 
            'e1_end': self.e1_end, 
            'e2': self.e2_str, 
            'e2_start': self.e2_start, 
            'e2_end': self.e2_end, 
            'relation': self.relation, 
            'relation_score': self.get_relation_score()
        }
        return relation_dict

class Abstract:
    def __init__(self, doc_key):
        self.doc_key = doc_key 
        self.relation_score = -1
        self.relations = []
        self.closest_relation = None

        # Load extra information
        self.sentences = FINKB_SENTENCES[str(self.doc_key)]
        abstract_extra_df = FINKB_EXTRAINFO.loc[FINKB_EXTRAINFO.id == self.doc_key].iloc[0]
        self.authors = abstract_extra_df.authors
        self.abstract = abstract_extra_df.abstract
        self.title = abstract_extra_df.title 
        self.doi = abstract_extra_df.doi 
        self.date = abstract_extra_df.date 
        self.source = abstract_extra_df.journal
    
    def get_relation_score(self):
        return self.relation_score

    def get_doc_key(self):
        return self.doc_key
    
    def add_relation(self, new_relation, new_relation_score):
        # create new relation
        new_relation_obj = Relation(new_relation, new_relation_score)

        # update relation score
        if self.relation_score < new_relation_score:
            self.closest_relation = new_relation_obj
            self.relation_score = new_relation_score

        # add relation
        self.relations.append(new_relation_obj)


    def __lt__(self, other):
        return self.get_relation_score() < other.get_relation_score()

    def to_dict(self):
        abstract_dict = {
            "doc_key": self.get_doc_key(), 
            "relation_score": self.get_relation_score(), 
            "relations": [x.to_dict() for x in self.relations],
            "closest_relation": self.closest_relation.to_dict(),
            "authors": self.authors,
            "sentences": self.sentences,
            "title": self.title,
            "doi": self.doi, 
            "date": self.date, 
            "source": self.source
        }
        return abstract_dict
    

