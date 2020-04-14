import requests
import logging
from bs4 import BeautifulSoup

"""
 Variables that are preced by ** _ ** char are bs4 object
"""

ATECO_CODES_PAGE_URL = 'https://www.codiceateco.it/sezioni'


def scrape():
    ateco_main_page = requests.get(ATECO_CODES_PAGE_URL)

    _ateco_main_page = BeautifulSoup(ateco_main_page.content, 'html.parser')
    __ateco_main_page = _ateco_main_page.prettify()

    print(__ateco_main_page)
