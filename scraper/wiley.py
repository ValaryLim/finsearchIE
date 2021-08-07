import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

def scrape_journal_of_finance(cwd):
    min_year = 1990
    min_volume_no = 45
    max_volume_no = datetime.now().year + min_volume_no - min_year + 1

    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
                
    for volume_no in tqdm.tqdm(range(min_volume_no, max_volume_no)):
        for issue_no in range(1, 7):
            volume_year = min_year + volume_no - min_volume_no - 1
            try:
                issue_page = requests.get(f'https://onlinelibrary.wiley.com/toc/15406261/{str(volume_year)}/{str(volume_no)}/{str(issue_no)}', 
                                    headers=headers)
                issue_soup = BeautifulSoup(issue_page.content, features="html.parser")

                articles = issue_soup.findAll('div', {'class': 'issue-item'})
                for article in articles:
                    try:
                        title = article.find('a', {'class': 'issue-item__title'}).text
                        link = f"https://onlinelibrary.wiley.com{article.find('a', {'class': 'issue-item__title'})['href']}"
                        doi = link.split('doi/')[1]
                        date_str = article.find('li', {'class': 'ePubDate'}).findAll('span')[1].text.strip()
                        date = datetime.strptime(date_str, '%d %B %Y').date()
                        authors = article.find('div', {'class': 'loa-authors-trunc'}).findAll('span', {'class': 'author-style'})
                        authors = [x.text.strip().title() for x in authors]

                        article_page = requests.get(link, headers=headers)
                        article_soup = BeautifulSoup(article_page.content, features="html.parser")
                        abstract = article_soup.find('div', {'class': 'article-section__content'}).p.text
                        abstract = " ".join(abstract.strip().split())
                        
                        df = df.append(
                            {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                            'date': date, 'journal':'Journal of Finance'}, \
                            ignore_index=True)
                    except:
                        continue
            except:
                continue

    df.to_csv(f'{cwd}/data/journal_of_finance.csv', index=False)