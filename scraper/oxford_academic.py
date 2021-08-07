import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

def scrape_quarterly_journal_of_economics(cwd):
    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    page = requests.get(f'https://academic.oup.com/qje/search-results?f_ContentType=Journal+Article&fl_SiteID=5504&page=1',\
            headers=headers)
    soup = BeautifulSoup(page.content, features="html.parser")
    total_articles = int(soup.find('div', {'class': 'sr-statistics'}).text.split(' of ')[1])//20
    
    for i in tqdm.tqdm(range(1, total_articles)):
        page = requests.get(f'https://academic.oup.com/qje/search-results?f_ContentType=Journal+Article&fl_SiteID=5504&page={str(i)}',\
            headers=headers)
        soup = BeautifulSoup(page.content, features="html.parser")

        for article in soup.findAll('div', {'class':'al-article-box'}):
            try:
                title = article.find('h4', {'class': 'sri-title'}).a.text
                authors = [x.text for x in article.findAll('a', {'class': 'author-link'})]
                link = article.find('div', {'class': 'al-citation-list'}).a['href']
                doi = link.split('doi.org/')[1]
                date_str = article.find('div', {'class': 'sri-date'}).text.split(': ')[1]
                date = datetime.strptime(date_str, '%d %B %Y').date()
                
                article_response = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_response.content, features='html.parser')
                abstract = article_soup.find('section', {'class': 'abstract'}).text
                
                df = df.append(
                    {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                    'date': date, 'journal':'The Quarterly Journal of Economics'}, \
                    ignore_index=True)
            except:
                continue

    df.to_csv(f'{cwd}/data/quarterly_journal_of_economics.csv', index=False)

def scrape_review_of_financial_studies(cwd):
    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    page = requests.get(f'https://academic.oup.com/rfs/search-results?f_ContentType=Journal+Article&fl_SiteID=5511&page=1',\
            headers=headers)
    soup = BeautifulSoup(page.content, features="html.parser")
    total_articles = int(soup.find('div', {'class': 'sr-statistics'}).text.split(' of ')[1])//20
    for i in tqdm.tqdm(range(1, total_articles)):
        page = requests.get(f'https://academic.oup.com/rfs/search-results?f_ContentType=Journal+Article&fl_SiteID=5511&page={str(i)}',\
            headers=headers)
        soup = BeautifulSoup(page.content, features="html.parser")

        for article in soup.findAll('div', {'class':'al-article-box'}):
            try:
                title = article.find('h4', {'class': 'sri-title'}).a.text
                authors = [x.text for x in article.findAll('a', {'class': 'author-link'})]
                link = article.find('div', {'class': 'al-citation-list'}).a['href']
                doi = link.split('doi.org/')[1]
                date_str = article.find('div', {'class': 'sri-date'}).text.split(': ')[1]
                date = datetime.strptime(date_str, '%d %B %Y').date()
                
                article_response = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_response.content, features='html.parser')
                abstract = article_soup.find('section', {'class': 'abstract'}).text
                
                df = df.append(
                    {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                    'date': date, 'journal':'The Quarterly Journal of Economics'}, \
                    ignore_index=True)
            except:
                continue
            break
        print(df)

    df.to_csv(f'{cwd}/data/review_of_financial_studies.csv', index=False)