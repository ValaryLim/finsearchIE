import os
import ast
import paperscraper
import pandas as pd

if __name__ == "__main__":
    keywords_path = 'keywords.txt'
    pubmed_dir = 'data/pubmed'

    # create directory if does not exist
    if not os.path.exists(pubmed_dir):
        os.makedirs(pubmed_dir)

    # retrieve keywords
    with open(keywords_path) as file:
        lines = [line.rstrip() for line in file]

    for query in lines:
        if not isinstance(query, str):
            raise TypeError(f'Pass str not {type(query)}')
        
        query_filename = '_'.join(query.lower().split(' '))
        paperscraper.pubmed.get_and_dump_pubmed_papers([query], output_filepath=f'data/pubmed/{query_filename}.txt')
        
        df = pd.DataFrame()
        with open(f'{pubmed_dir}/{query_filename}.txt', 'r') as f:
            for line in f:
                line_dict = ast.literal_eval(line)
                df = df.append(line_dict, ignore_index=True)
        df.to_csv(f'{pubmed_dir}/{query_filename}.csv', index=False)