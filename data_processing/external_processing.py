'''
Processes external_data.csv file into format accepted by Prodigy.
'''
import json
import pandas as pd
pd.options.display.max_rows = 999

if __name__ == "__main__":
    data_external = pd.read_csv('data/external/external_data.csv')

    # represent each unique article in the format {'text': article, 'meta': {'id': article_id}}
    prev_article = ''
    curr_id = 0
    articles = []
    for ind, row in data_external.iterrows():
        if (row['Article Title'] != prev_article) and (type(row['Abstract']) == str):
            prev_article = row['Article Title']
            curr_id += 1
            articles.append({'text': row['Abstract'], 'meta': {'id': "ZR" + str(curr_id)}})
    
    # convert to json format
    with open('data/external/external_zhiren.json', 'w') as jsonfile:
        json.dump(articles, jsonfile)