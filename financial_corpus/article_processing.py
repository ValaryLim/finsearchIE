'''
Combines and cleans each of the raw article .csv files and saves all articles into 1 file. 
Assigns unique article IDs to each article. 
'''
import os
import sys
import re
import json
import logging
import glob
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')

PUBLISHER_SITES = [
    'semantic_scholar', 'elsevier', 'oxford_academic', 'springer', \
    'american_accounting', 'american_economic', 'wiley'
]

def combine_csv(from_dir, to_dir, filename):
    print(from_dir, to_dir, filename)
    csvs = []
    for csv_filename in glob.glob(f"{from_dir}/*.csv"):
        csv_file = pd.read_csv(csv_filename, low_memory=False)
        csv_file['source'] = csv_filename.split('/')[-1].split('.')[0]
        csvs.append(csv_file)
    df = pd.concat(csvs, axis=0)
    df = df[['abstract', 'authors', 'title', 'doi', 'date', 'journal', 'source']]
    df.to_csv(f'{to_dir}/{filename}', index=False)

def label_id(df):
    df = df.reset_index(drop=True)
    df['id'] = df.index
    return df

def remove_redundant_words(text):
    text_lower = text.lower().strip()
    if 'article' in text_lower[:8]:
        return text.strip()[8:].strip()
    elif 'summary' in text_lower[:7]:
        return text.strip()[7:].strip()
    else:
        return text

def clean_field(df, field='abstract'):
    # ensure that field is not null
    condition1 = (df[field] != '')
    condition2 = (df[field] != None)
    condition3 = (df[field] != np.nan)
    condition4 = (~df[field].isnull())
    df = df[(condition1) & (condition2) & (condition3) & (condition4)] # not empty
    # remove in-text citations
    df[field] = df[field].apply(lambda x: re.sub(r"\s\([A-Z][a-z]+,\s[A-Z][a-z]?\.[^\)]*,\s\d{4}\)", "", x))
    df[field] = df[field].apply(lambda x: re.sub(r"\[.*?\]", "", x))
    # remove 'article' and 'summary'
    df[field] = df[field].apply(lambda x: remove_redundant_words(x))
    return df

def split_paragraph(df, field='abstract'):
    df['sentence'] = df[field].apply(lambda x: nltk.tokenize.sent_tokenize(str(x)))
    df = df.explode('sentence')
    df = df.dropna(subset=['sentence'])
    df['sentence'] = df['sentence'].apply(lambda x: x.strip().capitalize())
    df = df[df.sentence.apply(lambda x: len(x.split(' ')) > 4)]
    df = df.reset_index(drop=True)
    return df

def combine_publisher(source_dir, dest_dir, publisher_sites): 
    for publisher in publisher_sites:
        from_dir = f'{source_dir}/{publisher}'
        filename = f'{publisher}.csv'
        combine_csv(from_dir=from_dir, to_dir=dest_dir, filename=filename)

def create_abstract_label_template(abstract):
    abstract_word_list = nltk.word_tokenize(abstract)
    processed_abstract_word_list = []
    d = {}
    for word in abstract_word_list:
        if word in d:
            d[word] += 1
            processed_abstract_word_list.append(word + f'_{d[word]}')
        else:
            d[word] = 0
            processed_abstract_word_list.append(word + '_0')
    processed_abstract = ' '.join(processed_abstract_word_list)
    return f'''<abstractorig>{abstract}</abstractorig><abstract>{processed_abstract}</abstract><relations></relations><clusters></clusters>'''

if __name__ == "__main__":
    logger.info('Setting Up Workspace')

    root_dir = 'data'
    publishers_dir = f'{root_dir}/publishers'
    abstracts_dir = f'{root_dir}/abstracts'

    # create directories if don't exist
    if not os.path.exists(publishers_dir):
        os.makedirs(publishers_dir)
    if not os.path.exists(abstracts_dir):
        os.makedirs(abstracts_dir)

    # combine same publisher journals into one .csv
    combine_publisher(root_dir, publishers_dir, PUBLISHER_SITES)

    # combine all abstracts
    combine_csv(from_dir=publishers_dir, to_dir=abstracts_dir, filename="raw_abstracts.csv")

    # clean abstracts
    abstracts_df = pd.read_csv(f'{abstracts_dir}/raw_abstracts.csv')
    abstracts_df = abstracts_df.dropna() # remove rows with nan
    abstracts_df = clean_field(abstracts_df, field='abstract') # clean abstract field
    abstracts_df = abstracts_df.drop_duplicates(subset=['doi']) # drop duplicates
    abstracts_df = label_id(abstracts_df) # label abstracts
    abstracts_df.to_csv(f'{abstracts_dir}/abstracts.csv', index=False) # save

    # extract sentences
    sentences_df = split_paragraph(abstracts_df)[["id", "sentence"]]
    sentences_df.to_csv(f'{abstracts_dir}/sentences.csv', index=False)

    # sample abstracts and convert to json format
    abstracts_300_df = abstracts_df.sample(n=300, random_state=4101) # sample 300 abstracts
    abstracts_300_list = []
    for row_ind, row in abstracts_300_df.iterrows():
        doc_id = row['id']
        abstract = row['abstract']
        abstracts_300_list.append({'text': abstract, 'meta': {'id': doc_id }})
    with open(f'{abstracts_dir}/sample_abstracts.json', 'w') as jsonfile:
        json.dump(abstracts_300_list, jsonfile)