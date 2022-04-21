import json 

data_list = [
    'finsearch_backend/embedder/finsearch_embedder/data/finbert/coarse.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/finbert/granular.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/finmultiqa/coarse.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/finmultiqa/granular.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/msmarco/coarse.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/msmarco/granular.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/multiqa/coarse.jsonl',
    'finsearch_backend/embedder/finsearch_embedder/data/multiqa/granular.jsonl',
]

def load_jsonl(file_path):
    raw_data = []
    with open(file_path, "r") as f:
        for line in f:
            # read line
            json_line = json.loads(line)
            raw_data.append(json_line)
    return raw_data

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
        print("Relation Count", rel_map)
        print("Average Entity Length", ent_len_sum / ent_count)


    