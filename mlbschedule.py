# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:14:28 2022

@author: graig
"""

import requests
import json
from pandas import DataFrame, Series
import pandas as pd
from os import path
from glom import glom

DATA_DIR = '/Users/graig/Documents/BaseballBets/data'

with open(path.join(DATA_DIR, 'mlb_schedule.json')) as file:
    data = json.load(file)

MLB_schedule_url = 'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2022-4-7&endDate=2022-10-3'
df = pd.read_json(MLB_schedule_url)
df.info

df_nested_list = pd.json_normalize(
    data,
    record_path=['dates'],
    meta=['totalGames'])

df['dates'].apply(lambda row: glom(row,'gamePk'))

# requests for mlb schedule data
# def date_range(start_date, end_date):
#     search_endpoint = f'schedule/games/?sportId=1&startDate={start_date}&endDate={end_date}'
#     resp = requests.get(MLB_url + search_endpoint)
#     return resp.json()
    
# last_week = date_range(2022-5-26, 2022-5-27)

# then to turn it into json:
# last_week

# resp_sample = requests.get(sample_MLB_url)
# resp_sample.json()


brewers_dict = json.loads(clean_resp_text)['dates']['games']['row']
brewers_dict[0]

brewers_roster_df = DataFrame(brewers_dict)
brewers_roster_df.head()