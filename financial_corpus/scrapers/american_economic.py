import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

_american_economic_journals = {
    'aer': 'American Economics Review',
    'jel': 'Journal of Economic Literature',
    'jep': 'Journal of Economic Perspectives',
    'app': 'American Economic Journal Applied Economics',
    'pol': 'American Economic Journal Economic Policy',
    'mac': 'American Economic Journal Macroeconomics',
    'mic': 'American Economic Journal Microeconomics'
}

if __name__ == "__main__":
    american_economic_dir = 'data/american_economic'

    # create directory if does not exist
    if not os.path.exists(american_economic_dir):
        os.makedirs(american_economic_dir)
    
    # retrieve abstracts by journal
    for journal_id, journal_name in _american_economic_journals.items():
        # retrieve issues
        journal_response = requests.get(f'https://www.aeaweb.org/journals/{journal_id}/issues')
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
                # retrieve article details
                article_response = requests.get(article)
                article_soup = BeautifulSoup(article_response.content, features='html.parser')
                title = article_soup.find('meta', {'name': 'citation_title'})['content']
                authors = article_soup.find('ul', {'class': 'attribution'}).findAll('li', {'class': 'author'})
                authors = [x.text.strip() for x in authors]
                date_str = article_soup.find('meta', {'name': 'citation_publication_date'})['content']
                date = datetime.strptime(date_str, '%Y/%m').date()
                doi = article_soup.find('meta', {'name': 'citation_doi'})['content']
                abstract = str(article_soup.find('section', {'class': 'abstract'})).split('</h2>')[1].strip()
                abstract = abstract.split("</section>")[0].strip()
                df = df.append(
                    {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                    'date': date, 'journal':journal_name}, \
                    ignore_index=True)
            except:
                continue
        
        filename = "_".join(journal_name.lower().split(" ")) + ".csv"
        df.to_csv(f'{american_economic_dir}/{filename}', index=False)
    
    