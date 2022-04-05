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

# set working directory
sys.path.append(os.getcwd())
import utils

# get logger (debugger)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def combine_csv(from_dir, to_dir, filename):
    csvs = []
    for csv_filename in glob.glob(from_dir + '*.csv'):
        csv_file = pd.read_csv(csv_filename, low_memory=False)
        csv_file['source'] = csv_filename.split('/')[-1].split('.')[0]
        csvs.append(csv_file)
    df = pd.concat(csvs, axis=0)
    df = df[['abstract', 'authors', 'title', 'doi', 'date', 'journal', 'source']]
    df.to_csv(to_dir + filename, index=False)

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
    df[field] = df[(df[field] != '') & (df[field] != None) & (df[field] != np.nan) & (~df[field].isnull())] # not empty
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

def combine_publisher(article_dir, publisher_sites): 
    for publisher in publisher_sites:
        from_dir = f'{article_dir}{publisher}/'
        filename = f'{publisher}.csv'
        combine_csv(from_dir=from_dir, to_dir=article_dir, filename=filename)

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
    cwd = os.getcwd() # retrieve current working directory

    article_dir = f'{cwd}/data/articles/'
    publisher_sites = ['semantic_scholar', 'elsevier', 'oxford_academic', 'sagepub', 'pubmed', 'springer', \
        'american_accounting', 'american_economic', 'wiley']
    article_filtered_dirs = [f'{cwd}/data/articles_filtered/75_finance/']

    # combine same publisher journals into one .csv
    combine_publisher(article_dir, publisher_sites)
    
    # combine all articles into one .csv
    for filtered_dir in article_filtered_dirs:
        # create dir names
        raw_abstracts_dir = filtered_dir + 'raw_abstracts/'
        abstracts_dir = filtered_dir + 'abstracts/'
        sample_abstracts_dir = filtered_dir + 'sample_abstracts/'

        # clean abstracts
        combine_csv(from_dir=raw_abstracts_dir, to_dir=abstracts_dir, filename='abstracts.csv')
        abstracts_df = pd.read_csv(f'{abstracts_dir}abstracts.csv')
        abstracts_df = abstracts_df.dropna()
        abstracts_df = clean_field(abstracts_df, field='abstract') # clean
        abstracts_df = abstracts_df.drop_duplicates(subset=['doi']) # drop duplicates
        abstracts_df = label_id(abstracts_df) # label abstracts
        abstracts_df.to_csv(f'{abstracts_dir}abstracts_processed.csv', index=False) # save processed abstracts

        # extract sentences
        sentences_df = split_paragraph(abstracts_df)[["id", "sentence"]]
        sentences_df_1000 = sentences_df.sample(n=1000, random_state=4101)
        sentences_df.to_csv(f'{abstracts_dir}sentences_1000.csv', index=False)
        sentences_df.to_csv(f'{abstracts_dir}sentences.csv', index=False)

        # randomly sample abstracts 
        abstracts_2500 = abstracts_df.sample(n=2500, random_state=4101)

        # for each abstract
        for row_ind, row in abstracts_2500.iterrows():
            id = row['id']
            abstract = row['abstract']
            encoded_abstract = abstract.encode("utf8")
            with open(f'{sample_abstracts_dir}{id}.txt', 'wb') as f:
                f.write(encoded_abstract)

        # combine sampled abstracts into same json file
        samples = []
        for path in glob.glob(f'{sample_abstracts_dir}*.txt'):
            with open(path, "r") as f:
                txt = f.read()
                doc_id = path.split('/')[-1].split('.txt')[0]
                samples.append({'text': txt, 'meta': {'id': doc_id}})
        with open(f'{filtered_dir}sample.json', 'w') as jsonfile:
            json.dump(samples, jsonfile)

        print(filtered_dir)
        print('num abstracts:', len(abstracts_df))
        print('num sentences:', len(sentences_df))