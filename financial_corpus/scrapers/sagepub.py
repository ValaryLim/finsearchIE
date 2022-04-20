import os
import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

_sagepub_journals = {
    'aexb': {'min_year': 1960, 'min_volume_no': 4, 'journal_name': 'The American Economist', 'num_issues': 2},
    'anzb': {'min_year': 1993, 'min_volume_no': 1, 'journal_name': 'Australasian Marketing Journal', 'num_issues': 2},
    'ccha': {'min_year': 1995, 'min_volume_no': 1, 'journal_name': 'Competition and Change', 'num_issues': 5},
    'elra': {'min_year': 1990, 'min_volume_no': 1, 'journal_name': 'The Economic and Labour Relations Review', 'num_issues': 2},
    'edqa': {'min_year': 1987, 'min_volume_no': 1, 'journal_name': 'Economic Development Quarterly', 'num_issues': 4},
    'mrea': {'min_year': 2000, 'min_volume_no': 4, 'journal_name': 'International Journal of Market Research', 'num_issues': 6},
    'joma': {'min_year': 1975, 'min_volume_no': 1, 'journal_name': 'Journal of Management', 'num_issues': 8},
    'jmxa': {'min_year': 1970, 'min_volume_no': 34, 'journal_name': 'Journal of Marketing', 'num_issues': 6},
    'mrja': {'min_year': 1964, 'min_volume_no': 1, 'journal_name': 'Journal of Marketing Research', 'num_issues': 6}
}

def _scrape_sagepub_journal(journal_name, journal_id, min_year, min_volume_no, num_issues=6):
    max_volume_no  = datetime.now().year + min_volume_no - min_year + 1

    df = pd.DataFrame()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    
    for volume_no in tqdm.tqdm(range(min_volume_no, max_volume_no)):
        for issue_no in range(1, num_issues + 1):
            volume_year = min_year + volume_no - min_volume_no
            try:
                link = f'https://journals.sagepub.com/toc/{str(journal_id)}/{str(volume_no)}/{str(issue_no)}'
                issue_page = requests.get(link, headers=headers)
                issue_soup = BeautifulSoup(issue_page.content, features="html.parser")

                articles = issue_soup.findAll('div', {'class': 'art_title'})
                articles = [f"https://journals.sagepub.com{x.a['href']}" for x in articles]
                for article in articles:
                    try:
                        article_page = requests.get(article, headers=headers)
                        article_soup = BeautifulSoup(article_page.content, 'html.parser')
                        title = article_soup.find('div', {'class': 'publicationContentTitle'}).text.strip()
                        authors = list(set([x.a.text.strip() for x in article_soup.findAll('span', {'class': 'contribDegrees'})]))
                        date_str = article_soup.find('span', {'class': 'publicationContentEpubDate'}).text.split('Published')[1].strip()
                        date = datetime.strptime(date_str, '%B %d, %Y').date()
                        abstract = article_soup.find('div', {'class': 'abstractSection'}).p.text.strip()
                        doi = article_soup.find('a', {'class': 'doiWidgetLink'}).text.split('.org/')[1]

                        df = df.append(
                            {'abstract': abstract, 'authors': authors, 'title': title, 'doi': doi, \
                            'date': date, 'journal':journal_name}, \
                            ignore_index=True)
                    except:
                        continue
            except:
                continue
    return df

if __name__ == "__main__":
    sagepub_dir = 'data/sagepub'

    # create directory if does not exist
    if not os.path.exists(sagepub_dir):
        os.makedirs(sagepub_dir)

    for journal_id, journal_details in _sagepub_journals.items():
        journal_name = journal_details['journal_name']
        min_year = journal_details['min_year']
        min_volume_no = journal_details['min_volume_no']
        num_issues = journal_details['num_issues']
    
        df = _scrape_sagepub_journal(journal_name, journal_id, min_year, min_volume_no, num_issues)

        filename = "_".join(journal_name.lower().split(" ")) + ".csv"
        df.to_csv(f'{sagepub_dir}/{filename}', index=False)