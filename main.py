import os
import sys
import logging
import ast
import pandas as pd
import scraper

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info('Setting Up Workspace')
    # retrieve current working directory
    cwd = os.getcwd()

    # # retrieve queries
    # with open(f'{cwd}/keywords.txt') as f:
    #     queries = f.readlines()
    #     queries = [x.strip() for x in queries]

    # for query in queries:
    #     logger.info(f'Scraping Pubmed: {query}')
    #     scraper.query_pubmed(query, cwd)

    # logger.info('Scraping Quarterly Journal of Economics')
    # scraper.scrape_quarterly_journal_of_economics(cwd)
    # logger.info('Scraping The Review of Financial Studies')
    # scraper.scrape_review_of_financial_studies(cwd)
    logger.info('Scraping American Economics Review')
    scraper.scrape_american_economics_review(cwd)
    # logger.info('Scraping Accounting Review')
    # scraper.scrape_accounting_review(cwd)
    # logger.info('Scraping Journal of Finance')
    # scraper.scrape_journal_of_finance(cwd)