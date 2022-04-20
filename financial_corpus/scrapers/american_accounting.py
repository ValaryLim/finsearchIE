import os
import requests
from bs4 import BeautifulSoup
import tqdm
import pandas as pd
from datetime import datetime

_american_accounting_journals = {
    'accounting-review': {'journal_name': 'Accounting Review', 'min_year': 1999, 'min_volume_no': 74, 'num_issues': 6},
    'ahj': {'journal_name': 'Accounting Historians Journal', 'min_year':1974 , 'min_volume_no':1 , 'num_issues': 2},
    'api': {'journal_name': 'Accounting and the Public Interest', 'min_year':2001 , 'min_volume_no':1 , 'num_issues': 1},
    'ajpt': {'journal_name': 'Auditing Journal of Practice and Theory', 'min_year':1999 , 'min_volume_no':18, 'num_issues': 4},
    'bria': {'journal_name': 'Behavioral Research in Accounting', 'min_year':2001 , 'min_volume_no':13, 'num_issues': 2},
    'jeta': {'journal_name': 'Journal of Emerging Technologies in Accounting', 'min_year':2004 , 'min_volume_no':1, 'num_issues': 1},
    'jfr': {'journal_name': 'Journal of Financial Reporting', 'min_year':2016 , 'min_volume_no':1, 'num_issues': 2},
    'jogna': {'journal_name': 'Journal of Governmental and Nonprofit Accounting', 'min_year':2012 , 'min_volume_no':1, 'num_issues': 1},
    'jfar': {'journal_name': 'Journal of Forensic Accounting Research', 'min_year':2016 , 'min_volume_no':1, 'num_issues': 1},
    'jmar': {'journal_name': 'Journal of Management Accounting Research', 'min_year':2000 , 'min_volume_no':12, 'num_issues': 4},
    'jiar': {'journal_name': 'Journal of International Accounting Research', 'min_year':2002 , 'min_volume_no':1, 'num_issues': 4}
}

def _scrape_american_accounting_journal(journal_name, journal_id, min_year, min_volume_no, num_issues):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    max_volume_no  = datetime.now().year + min_volume_no - min_year + 1
    df = pd.DataFrame()
    for volume_no in tqdm.tqdm(range(min_volume_no, max_volume_no)):
        for issue_no in range(1, num_issues+1):
            try:
                page = requests.get(f'https://meridian.allenpress.com/{journal_id}/issue/{str(volume_no)}/{str(issue_no)}', 
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
                                'date': date, 'journal':journal_name}, \
                                ignore_index=True)
                    except:
                        continue
            except:
                continue
    return df

if __name__ == "__main__":
    american_accounting_dir = 'data/american_accounting'

    # create directory if does not exist
    if not os.path.exists(american_accounting_dir):
        os.makedirs(american_accounting_dir)
    
    # retrieve abstracts by journal
    for journal_id, journal_details in _american_accounting_journals.items():
        journal_name = journal_details['journal_name']
        min_year = journal_details['min_year']
        min_volume_no = journal_details['min_volume_no']
        num_issues = journal_details['num_issues']

        df = _scrape_american_accounting_journal(journal_name, journal_id, min_year, min_volume_no, num_issues)

        filename = "_".join(journal_name.lower().split(" ")) + ".csv"
        df.to_csv(f'{american_accounting_dir}/{filename}', index=False)
