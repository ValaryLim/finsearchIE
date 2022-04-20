import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

_oxford_academic_journals = {
    5186: 'Journal of Competition Law and Economics',
    5190: 'Journal of Economic Geography',
    5193: 'Journal of Financial Econometrics',
    5203: 'Journal of International Economic Law',
    5397: 'Journal of Consumer Research',
    5427: 'American Law and Economics Review',
    5437: 'Cambridge Journal of Economics',
    5438: 'Cambridge Journal of Regions Economy and Society',
    5440: 'CESifo Economic Studies',
    5473: 'Journal of Financial Regulation',
    5475: 'The Journal of Law Economics and Organization',
    5504: 'Quaryerly Journal of Economics',
    5511: 'Review of Financial Studies',
    5571: 'Journal of the Europea Economic Association',
    6178: 'The Econometrics Journal',
    6182: 'The Economic Journal'
}

if __name__ == "__main__":
    oxford_academic_dir = 'data/oxford_academic'

    # create directory if does not exist
    if not os.path.exists(oxford_academic_dir):
        os.makedirs(oxford_academic_dir)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    for journal_id, journal_name in _oxford_academic_journals.items():
        df = pd.DataFrame()
        page = requests.get(f'https://academic.oup.com/qje/search-results?f_ContentType=Journal+Article&fl_SiteID={str(journal_id)}&page=1',\
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
                    'date': date, 'journal':journal_name}, \
                    ignore_index=True)
            except:
                continue

        filename = "_".join(journal_name.lower().split(" ")) + ".csv"
        df.to_csv(f'{oxford_academic_dir}/{filename}', index=False)