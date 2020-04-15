import requests
import json
from bs4 import BeautifulSoup

"""
 Variables that are preced by ** _ ** char are bs4 object
"""

ATECO_CODES_PAGE_URL = 'https://www.codiceateco.it'
ATECO_CODES_PAGE_SECTION_URL = 'https://www.codiceateco.it/sezioni'


def scrape():
    ateco_main_page = requests.get(ATECO_CODES_PAGE_SECTION_URL)
    _ateco_main_page = BeautifulSoup(ateco_main_page.content, 'html.parser')
    
    sections = parse_page(_ateco_main_page)
    
    # per ogni sezione mi calcolo le divisioni
    for section in sections:
        division_page = requests.get(ATECO_CODES_PAGE_URL + section['link'])
        _division_page = BeautifulSoup(division_page.content, 'html.parser')
        section['divisions'] = parse_page(_division_page)
        
        # per ogni divisione calcolo i gruppi 
        for division in section['divisions']:
            group_page = requests.get(ATECO_CODES_PAGE_URL + division['link'])
            _group_page = BeautifulSoup(group_page.content, 'html.parser')
            division['groups'] = parse_page(_group_page)
            
            # per ogni gruppo calcolo le classi
            for group in division['groups']:
                group_page = requests.get(ATECO_CODES_PAGE_URL + group['link'])
                _group_page = BeautifulSoup(group_page.content, 'html.parser')
                group['classes'] = parse_page(_group_page)
                
                # per ogni classe recupero i codici ateco
                for a_class in group['classes']:
                    ateco_page = requests.get(ATECO_CODES_PAGE_URL + a_class['link'])
                    _ateco_page = BeautifulSoup(ateco_page.content, 'html.parser')
                    a_class['codes'] = parse_page(_ateco_page)

                    for ateco in a_class['codes']:
                        ateco = get_ateco_code_info(ateco)
                        print('Section[{}] | Division[{}] | Group[{}] | Class[{}] | Code[{}]'.format(section['code'], division['code'], group['code'], a_class['code'], ateco['code']))

    ateco_codes = get_only_ateco_codes(sections)

    with open('ateco_codes_structure.json', 'w') as outfile:
        json.dump(sections, outfile)
    
    with open('ateco_codes.json', 'w') as outfile:
        json.dump(ateco_codes, outfile)
    


def parse_page(soup):
    data = []
    
    table = soup.find('table')
    rows = table.find_all('tr')
 
    for row in rows:
        cols = row.find_all('td')
        parsed_cols = [ele.text.strip() for ele in cols]

        info = {
                'code': parsed_cols[0],
                'name': parsed_cols[1],
                'link': None,
                }
        
        # cerco il link
        for col in cols:
            for a in col.find_all('a', href=True):
                info['link'] = a['href']
        
        data.append(info)
        
        # data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data

def get_ateco_code_info(ateco_object):
    ateco_code_page = requests.get(ATECO_CODES_PAGE_URL + ateco_object['link'])
    _ateco_code_page = BeautifulSoup(ateco_code_page.content, 'html.parser')
    
    page = _ateco_code_page.find('section', class_='ateco-result')
    if page is None:
        return ateco_object

    description = page.find('ul')
    if description is None:
        return ateco_object

    description_list = [li.text.strip() for li in description.find_all('li')]
    ateco_object['description'] = description_list
    return ateco_object

def get_only_ateco_codes(ateco_strucures, append_structure_info = False):
    data = []
    for section in ateco_strucures:
        for division in section['divisions']:
            for group in division['groups']:
                for _class in group['classes']:
                    for ateco in _class['codes']:
                        print(ateco)
                        ateco_obj = {
                                'name': ateco['name'], 
                                'ateco': ateco['code'], 
                                'description': '\n'.join(ateco.get('description', '')), 
                            }

                        if append_structure_info:
                            ateco_obj.update({
                                    'section': section['code'],
                                    'division': division['code'],
                                    'group': group['code'],
                                    'class': group['code'],
                                })
                        data.append(ateco_obj)
    return data

