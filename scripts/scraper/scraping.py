import os
import sys
import logging
import ast
import json
import pandas as pd

import utils
import scraper

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

scrapers = {
    # 'American Economics Review': scraper.scrape_american_economics_review,
    'Sagepub': scraper.scrape_sagepub
    # 'American Accounting': scraper.scraper_american_accounting,
    # 'Wiley': scraper.scrape_wiley,
    # 'Oxford Academic': scraper.scrape_oxford_academic
}

if __name__ == "__main__":
    logger.info('Setting Up Workspace')
    # retrieve current working directory
    cwd = os.getcwd()
    scraper_path = f'{cwd}/data/articles'
    with open(f'{cwd}/utils/config.json') as f:
        config = json.load(f)
    
    # retrieve queries
    # queries = utils.convert_txt_to_list(f'{cwd}/data/query/keywords.txt')

    # for query in queries:
    # 	logger.info(f'Scraping Pubmed: {query}')
    # 	scraper.query_pubmed(query, scraper_path)

    #     logger.info(f'Scraping Elsevier: {query}')
    #     scraper.query_elsevier(query, scraper_path, config=config['elsevier'])

    springer_journals = utils.convert_txt_to_list(f'{cwd}/data/query/springer_journals.txt')
    for journal in springer_journals[35:]:
        logger.info(f'Scraping Springer: {journal}')
        scraper.scrape_springer_journal(journal, scraper_path)

    # for scraper_name, scraper_fn in scrapers.items():
    #     logger.info(f'Scraping {scraper_name}')
    #     scraper_fn(scraper_path)
