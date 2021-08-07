import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

def scrape_accounting_review(cwd):
    min_volume_no = 74
    max_volume_no = datetime.now().year + min_volume_no - 1999 + 1 # volumes start in 1999
    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}

    for volume_no in tqdm.tqdm(range(74, max_volume_no)):
        for issue_no in range(1, 7):
            try:
                page = requests.get(f'https://meridian.allenpress.com/accounting-review/issue/{str(volume_no)}/{str(issue_no)}', 
                                    headers=headers)
                soup = BeautifulSoup(page.content, features="html.parser")

                for article in soup.findAll('div', {'class': 'al-article-items'}):
                    try:
                        link = f"https://meridian.allenpress.com{article.a['href']}"
                        title = article.a.text
                        article_page = requests.get(link, headers=headers)
                        article_soup = BeautifulSoup(article_page.content, features="html.parser")
                        authors = article_soup.findAll('div', {'class': 'al-author-name'})
                        authors = [x.a.text.strip() for x in authors]
                        doi = article_soup.find('div', {'class': 'citation-doi'}).a['href'].split('.org/')[1]
                        abstract = article_soup.find('section', {'class': 'abstract'}).p.text.strip()
                        date_str = article_soup.find('span', {'class': 'article-date'}).text
                        date = datetime.strptime(date_str, '%B %d %Y').date()
                        
                        if len(authors):
                            df = df.append(
                                {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                                'date': date, 'journal':'Accounting Review'}, \
                                ignore_index=True)
                    except:
                        continue
            except:
                continue
    df.to_csv(f'{cwd}/data/accounting_review.csv', index=False)
