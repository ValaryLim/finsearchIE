from elsapy.elsclient import ElsClient
from elsapy.elssearch import ElsSearch
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus as url_encode

def _search_elsevier(client, query, total_count=5000):
    base_url = u'https://api.elsevier.com/content/search/'
    domain = 'scopus'
    uri = base_url + domain + '?query=' + url_encode(query)
    iterations = total_count // 25 - 1
    
    api_response = client.exec_request(uri)
    results = api_response['search-results']['entry']
    
    prev_url = ''
    for i in range(iterations):
        try:
            for e in api_response['search-results']['link']:
                if e['@ref'] == 'next':
                    next_url = e['@href']
                    break
        
            if next_url == prev_url: # stop process if no more new urls
                break
            api_response = client.exec_request(next_url)
            results += api_response['search-results']['entry']
            prev_url = next_url
        except:
            break
    return results


def query_elsevier(query, path, config):
    headers = {
        'X-ELS-APIKey': config['apikey'],
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    client = ElsClient(config['apikey'])

    search_results = _search_elsevier(client, f"KEY({query.lower()})")
    
    # retrieve articles
    df = pd.DataFrame()
    for article in search_results:
        try:
            doi = article['prism:doi']
            title = article['dc:title']
            journal = article['prism:publicationName']
            date = article['prism:coverDate']
            
            pii = article['pii']
            article_page = requests.get(f'https://www.sciencedirect.com/science/article/abs/pii/{pii}', headers=headers)
            article_soup = BeautifulSoup(article_page.content, features='html.parser')
            abstract = article_soup.select('div.abstract.author')[0].p.text
            authors = article_soup.findAll('a', {'class': 'author'})
            authors = [x.find('span', {'class': 'given-name'}).text + ' ' +  x.find('span', {'class': 'surname'}).text for x in authors]
            # append to dataframe
            df = df.append(
                {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                'date': date, 'journal':journal}, ignore_index=True
            )
        except:
            continue
    
    query_filename = '_'.join(query.lower().split(' '))
    df.to_csv(f'{path}/elsevier/{query_filename}.csv', index=False)
