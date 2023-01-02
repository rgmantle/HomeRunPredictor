# -*- coding: utf-8 -*-
"""
Created on Sun May 29 22:27:41 2022

@author: graig
"""

from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

stadiums_res = requests.get('https://ballparkpal.com/ParkFactors2.php', headers=HEADERS)

stadium_soup = Soup(stadiums_res.text)

tables = stadium_soup.find_all('table')

stadium_table = tables[0]

rows = stadium_table.find_all('tr')

first_data_row = rows[1]

[str(x.string) for x in first_data_row.find_all('td')]

def parse_row(row):
    return [str(x.string) for x in row.find_all('td')]

list_of_parsed_rows = [parse_row(row) for row in rows[1:-1]]

stadium_df = DataFrame(list_of_parsed_rows)
stadium_df.columns = ["stadium", "hr", "xbh", "runs"]

all_link_tags = stadium_soup.find_all('a')

def stadium_names(row):
    return [str(x.string) for x in row.find_all('a')]

stadiums = [stadium_names(row) for row in rows[1:34]]
stadnames_df = DataFrame(stadiums)        
stadnames_df.columns = ["stadium"]    

            

