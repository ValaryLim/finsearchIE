import os
import pandas as pd
import numpy as np

if __name__ == "__main__":
    # data directories
    data_dirs = [
        "data/macaw/rel_comb/finance/coarse_coref/", "data/macaw/rel_comb/finance/granular_coref/", \
        "data/macaw/rel_comb/external_zhiren/coarse/", "data/macaw/rel_comb/external_zhiren/granular/", \
        "data/macaw/rel_perm/finance/coarse_coref/", "data/macaw/rel_perm/finance/granular_coref/", \
        "data/macaw/rel_perm/external_zhiren/coarse/", "data/macaw/rel_perm/external_zhiren/granular/"
    ]

    for filedir in data_dirs:
        for filename in os.listdir(filedir):
            df = pd.read_csv(filedir + filename)
            df['sentence_id'] = ((df['sentence'] != df['sentence'].shift()).astype(int)).cumsum()

            # count the average number of pairs in each sentence
            num_pairs = df['sentence_id'].value_counts().mean()
            num_no_rel = df[df["R"].isna()]['sentence_id'].value_counts().sum() / max(df['sentence_id'])
            num_rel = df[~df["R"].isna()]['sentence_id'].value_counts().sum() / max(df['sentence_id'])
            print(filedir + filename)
            print("Average Number of Pairs Per Sentence:", num_pairs)
            print("Average Number of Pairs with No Relation:", num_no_rel)
            print("Percentage of Pairs with No Relation:", num_no_rel/num_pairs)
            print("Average Number of Pairs with Relations:", num_rel)
            print("Percentage of Pairs With Relation:", num_rel/num_pairs)
            for relation in df[~df["R"].isna()]["R"].unique():
                num_rel = df[df["R"] == relation]['sentence_id'].value_counts().sum() / max(df['sentence_id'])
                print(f"Average Number of Pairs with {relation} Relation:", num_rel)
                print(f"Percentage of Pairs with {relation} Relation:", num_rel/num_pairs)
            print("------------------------------------------------")