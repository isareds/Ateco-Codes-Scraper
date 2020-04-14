import requests
import logging

from bs4 import BeautifulSoup

ATECO_CODES_PAGE_URL = 'https://www.codiceateco.it/sezioni'
ateco_main_page = requests.get(ATECO_CODES_PAGE_URL)

_ateco_main_page = BeautifulSoup(ateco_main_page.content, 'html.parser')



