import os
import sys
sys.path.append(os.getcwd())
import utils

data_list = [
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/finbert/coarse.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/finbert/granular.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/finmultiqa/coarse.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/finmultiqa/granular.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/msmarco/coarse.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/msmarco/granular.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/multiqa/coarse.jsonl',
    '/Users/valarylim/financeOpenIE/finsearch_backend_embedding/data/multiqa/granular.jsonl',
]

if __name__ == "__main__":
    for data_name in data_list:
        print(data_name)
        data = utils.load_jsonl(data_name)
        # count number of relations
        rel_map = {}
        ent_len_sum, ent_count = 0, 0
        for row in data:
            row_rel, row_e1, row_e2 = row["REL"], row["E1"], row["E2"]
            if row_rel in rel_map:
                rel_map[row_rel] += 1
            else:
                rel_map[row_rel] = 1
            
            ent_len_sum += len(row_e1.split(" "))
            ent_len_sum += len(row_e2.split(" "))
            ent_count += 2
        print(rel_map)
        print("avg ent len", ent_len_sum / ent_count)


    