import ast
import paperscraper
import pandas as pd

def query_pubmed(query, cwd):
    if not isinstance(query, str):
        raise TypeError(f'Pass str not {type(query)}')
    
    query_filename = '_'.join(query.lower().split(' '))
    paperscraper.pubmed.get_and_dump_pubmed_papers([query], output_filepath=f'data/pubmed/{query_filename}.txt')
    
    df = pd.DataFrame()
    with open(f'{cwd}/data/pubmed/{query_filename}.txt', 'r') as f:
        for line in f:
            line_dict = ast.literal_eval(line)
            df = df.append(line_dict, ignore_index=True)
    df.to_csv(f'{cwd}/data/pubmed/{query_filename}.csv', index=False)