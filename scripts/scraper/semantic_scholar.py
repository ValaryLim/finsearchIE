import pandas as pd
import requests
import datetime
import time
import json

def query_semantic_scholar(query, path, fields=['Economics', 'Business']):
    limit = 100
    offset = 0
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

    df = pd.DataFrame()
    while True:
        api_response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={str(offset)}&limit={str(limit)}&fields=title,abstract,authors,externalIds,year,fieldsOfStudy', \
                                headers=headers)
        api_content = json.loads(api_response.content)
        try:
            articles = api_content['data']
        except:
            time.sleep(60) # wait for 1min
            print("response error. re-query data.")
            continue

        if len(articles) == 0 or 'next' not in api_content:  # no articles remaining
            break

        offset = api_content['next']
            
        for article in articles:
            try:
                title = article['title']
                doi = article['externalIds']['DOI']
                abstract = article['abstract'].strip()
                date = datetime.date(article['year'], 1, 1)
                topics = article['fieldsOfStudy']
                relevant = any([x in fields for x in topics])
                authors = article['authors']
                authors = [x['name'] for x in article['authors']]

                if relevant:
                    df = df.append(
                        {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                        'date': date, 'journal':'Semantic Scholar'}, \
                        ignore_index=True)
            except:
                continue
    
    query_filename = '_'.join(query.lower().split(' '))
    df.to_csv(f'{path}/semantic_scholar/{query_filename}.csv', index=False)
