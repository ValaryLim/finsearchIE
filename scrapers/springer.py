import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import tqdm
import utils

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
}

def retrieve_journals(path):
    journals = []
    for i in range(1, 11):
        # economics search
        query_link = f'https://www.springer.com/gp/product-search/discipline?disciplineId=economics&facet=type__journal&page={str(i)}&returnUrl=gp%2Feconomics&topic=911020%2CW00000%2CW28000%2CW28010%2CW28020%2CW29000%2CW29010%2CW29020%2CW29030%2CW31000%2CW31010%2CW31020%2CW32000%2CW33000%2CW33010%2CW34000%2CW34020%2CW34030%2CW35000%2CW36000%2CW37000%2CW38000%2CW39000%2CW41000%2CW42000%2CW43000%2CW44000%2CW45000%2CW45010%2CW46000%2CW47000%2CW48000%2CW48010%2CW49000%2CW49010%2CW51000%2CW52000'
        query_page = requests.get(query_link, headers=headers)
        query_soup = BeautifulSoup(query_page.content, 'html.parser')
        query_journals = query_soup.findAll('div', {'class': 'result-type-journal'})
        query_journals = [f"https://link.springer.com{x.a['href']}/volumes-and-issues" for x in query_journals]
        journals.extend(query_journals)

        # business and management search
        query_link = f'https://www.springer.com/gp/product-search/discipline?disciplineId=businessmanagement&facet-type=type__journal&page={str(i)}&returnUrl=gp%2Fbusiness-management&topic=500000%2C511000%2C511010%2C511020%2C512000%2C513000%2C513010%2C513020%2C513030%2C513040%2C513050%2C514000%2C514010%2C514020%2C514030%2C515000%2C515010%2C515020%2C515030%2C515040%2C516000%2C517000%2C517010%2C517020%2C517030%2C518000%2C519000%2C519010%2C519020%2C519030%2C519040%2C521000%2C522000%2C522010%2C522020%2C522030%2C522040%2C522050%2C522060%2C522070%2C523000%2C524000%2C524010%2C525000%2C525010%2C526000%2C526010%2C526020%2C527000%2C527010%2C527020%2C527030%2C527040%2C527050%2C527060%2C527070%2C527080%2C528000%2C600000%2C611000%2C612000%2C613000%2C613010%2C613020%2C614000%2C615000%2C616000%2C617000%2C618000%2C619000%2C621000%2C622000'
        query_page = requests.get(query_link, headers=headers)
        query_soup = BeautifulSoup(query_page.content, 'html.parser')
        query_journals = query_soup.findAll('div', {'class': 'result-type-journal'})
        query_journals = [f"https://link.springer.com{x.a['href']}/volumes-and-issues" for x in query_journals]
        journals.extend(query_journals)
    
    utils.convert_list_to_txt(journals, f'{path}/springer_journals.txt')

def scrape_springer_journal(journal, path):
    journal_page = requests.get(journal, headers=headers)
    journal_soup = BeautifulSoup(journal_page.content, 'html.parser')
    issues = journal_soup.findAll('a', {'class': 'u-interface-link'})
    issues = [f"https://link.springer.com{x['href']}" for x in issues]
    
    df = pd.DataFrame()
    for issue in tqdm.tqdm(issues):
        issue_page = requests.get(issue, headers=headers)
        issue_soup = BeautifulSoup(issue_page.content, 'html.parser')
        articles = issue_soup.findAll('div', {'class': 'c-card__body'})
        
        for article in articles:
            try:
                title = article.find('h3', {'class': 'c-card__title'}).text.strip()
                url = article.find('h3', {'class': 'c-card__title'}).a['href']
                doi = url.split('article/')[1]
                date_str = article.find('li', {'data-test': 'published-on'}).text.split(': ')[1]
                date = datetime.strptime(date_str, '%d %B %Y').date()
                authors = article.find('ul', {'class': 'c-author-list'}).findAll('span')
                authors = [x.text for x in authors]

                article_page = requests.get(url, headers=headers)
                article_soup = BeautifulSoup(article_page.content, 'html.parser')
                journal_name = article_soup.find('i', {'data-test': 'journal-title'}).text
                abstract = article_soup.find('div', {'id': 'Abs1-content'}).text
                
                df = df.append(
                        {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                        'date': date, 'journal':journal_name}, \
                        ignore_index=True)
            except:
                continue
        
    filename = "_".join(journal_name.lower().split(" ")) + ".csv"
    df.to_csv(f'{path}/springer/{filename}', index=False)