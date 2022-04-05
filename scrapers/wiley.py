import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

_wiley_journals = {
    '15406261': {'min_year': 1990, 'min_volume_no': 45, 'journal_name': 'Journal of Finance', 'num_issues': 6},
    '1475679x': {'min_year': 2001, 'min_volume_no': 39, 'journal_name': 'Journal of Accounting Research', 'num_issues': 6},
    '10991255': {'min_year': 1986, 'min_volume_no': 1, 'journal_name': 'Journal of Applied Econometrics', 'num_issues': 6},
    '10969934': {'min_year': 2000, 'min_volume_no': 20, 'journal_name': 'Journal of Futures Markets', 'num_issues': 12},
    '1467629x': {'min_year': 2000, 'min_volume_no': 40, 'journal_name': 'Accounting and Finance', 'num_issues': 6},
    '14678683': {'min_year': 1998, 'min_volume_no': 6, 'journal_name': 'Corporate Governance', 'num_issues': 6},
    '15406288': {'min_year': 1990, 'min_volume_no': 6, 'journal_name': 'Financial Review', 'num_issues': 4},
    '1099131x': {'min_year': 2000, 'min_volume_no': 19, 'journal_name': 'Journal of Forecasting', 'num_issues': 8},
    '10970266': {'min_year': 2000, 'min_volume_no': 21, 'journal_name': 'Strategic Management Journal', 'num_issues': 12},
    '15406229': {'min_year': 2000, 'min_volume_no': 28, 'journal_name': 'Real Estate Economics', 'num_issues': 4},
    '14678551': {'min_year': 2000, 'min_volume_no': 11, 'journal_name': 'British Journal of Management', 'num_issues': 4},
    '10991379': {'min_year': 2000, 'min_volume_no': 21, 'journal_name': 'Journal of Organizational Behavior', 'num_issues': 8}
}

def _scrape_wiley_journal(journal_name, journal_id, min_year, min_volume_no, num_issues=6):
    max_volume_no  = datetime.now().year + min_volume_no - min_year + 1

    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    
    for volume_no in tqdm.tqdm(range(min_volume_no, max_volume_no)):
        for issue_no in range(1, num_issues + 1):
            volume_year = min_year + volume_no - min_volume_no
            try:
                issue_page = requests.get(f'https://onlinelibrary.wiley.com/toc/{str(journal_id)}/{str(volume_year)}/{str(volume_no)}/{str(issue_no)}', 
                                    headers=headers)
                issue_soup = BeautifulSoup(issue_page.content, features="html.parser")

                articles = issue_soup.findAll('div', {'class': 'issue-item'})
                for article in articles:
                    try:
                        title = article.find('a', {'class': 'issue-item__title'}).text.strip()
                        link = f"https://onlinelibrary.wiley.com{article.find('a', {'class': 'issue-item__title'})['href']}"
                        doi = link.split('doi/')[1]
                        date_str = article.find('li', {'class': 'ePubDate'}).findAll('span')[1].text.strip()
                        date = datetime.strptime(date_str, '%d %B %Y').date()
                        authors = article.find('div', {'class': 'loa-authors-trunc'}).findAll('span', {'class': 'author-style'})
                        authors = [x.text.strip().title() for x in authors]

                        article_page = requests.get(link, headers=headers)
                        article_soup = BeautifulSoup(article_page.content, features="html.parser")
                        abstract = article_soup.find('div', {'class': 'article-section__content'}).p.text
                        abstract = " ".join(abstract.strip().split()).strip()
                        df = df.append(
                            {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                            'date': date, 'journal':journal_name}, \
                            ignore_index=True)
                    except:
                        continue
            except:
                continue
    
    return df

def scrape_wiley(path):
    for journal_id, journal_details in _wiley_journals.items():
        journal_name = journal_details['journal_name']
        min_year = journal_details['min_year']
        min_volume_no = journal_details['min_volume_no']
        num_issues = journal_details['num_issues']
        if num_issues > 6:
            df = _scrape_wiley_journal(journal_name, journal_id, min_year, min_volume_no, num_issues)

            filename = "_".join(journal_name.lower().split(" ")) + ".csv"
            df.to_csv(f'{path}/wiley/{filename}', index=False)
