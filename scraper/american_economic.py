import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

def scrape_american_economics_review(cwd):
    # retrieve issues
    journal_response = requests.get('https://www.aeaweb.org/journals/aer/issues')
    journal_soup = BeautifulSoup(journal_response.content, features='html.parser')
    issues = journal_soup.find('section', {'class': 'journal-preview-group'}).findAll('a')
    issues = [f'https://www.aeaweb.org{x["href"]}' for x in issues]

    # retrieve articles
    articles = []
    for issue in tqdm.tqdm(issues):
        issue_response = requests.get(issue)
        issue_soup = BeautifulSoup(issue_response.content, features='html.parser')
        issue_articles = issue_soup.findAll('article', {'class': 'journal-article'})[1:]
        issue_articles_filtered = []
        for article in issue_articles:
            try:
                issue_articles_filtered.append(f'https://www.aeaweb.org{article.a["href"]}')
            except:
                continue
        articles.extend(issue_articles_filtered)

    # retrieve article details
    df = pd.DataFrame()
    for article in tqdm.tqdm(articles):
        try:
            title = article_soup.find('meta', {'name': 'citation_title'})['content']
            authors = article_soup.find('ul', {'class': 'attribution'}).findAll('li', {'class': 'author'})
            authors = [x.text.strip() for x in authors]
            date_str = article_soup.find('meta', {'name': 'citation_publication_date'})['content']
            date = datetime.strptime(date_str, '%Y/%m').date()
            doi = article_soup.find('meta', {'name': 'citation_doi'})['content']
            abstract = str(article_soup.find('section', {'class': 'abstract'})).split('</h2>')[1].strip()
            df = df.append(
                {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                'date': date, 'journal':'American Economic Review'}, \
                ignore_index=True)
        except:
            continue

    df.to_csv(f'{cwd}/data/american_economics_review.csv', index=False)
    