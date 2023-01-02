# -*- coding: utf-8 -*-
"""
Created on Sun May 29 22:27:41 2022

@author: graig
"""

from bs4 import BeautifulSoup as Soup
import pandas as pd
import requests
from pandas import DataFrame
from os import path

#code that is used throughout the file

DATA_DIR = '/Users/graig/Documents/BaseballBets'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#code to create stadium factor file
# stadiums_res = requests.get('https://ballparkpal.com/ParkFactors2.php', headers=HEADERS)

# stadium_soup = Soup(stadiums_res.text)

# tables3 = stadium_soup.find_all('table')

# stadium_table = tables3[0]

# rows3 = stadium_table.find_all('tr')

# first_data_row3 = rows3[1]

# [str(x.string) for x in first_data_row3.find_all('td')]

def parse_row(row):
    return [str(x.string) for x in row.find_all('td')]

# list_of_parsed_rows3 = [parse_row(row) for row in rows3[1:17]]

# stadium_df = DataFrame(list_of_parsed_rows3)
# stadium_df.columns = ["stadium", "hr", "xbh", "runs"]

# all_link_tags = stadium_soup.find_all('a')

# def stadium_names(row):
#     return [str(x.string) for x in row.find_all('a')]

# stadiums = [stadium_names(row) for row in rows3[1:34]]
# stadnames_df = DataFrame(stadiums)        
# stadnames_df.columns = ["stadium"]   
# stadium_df['stadium'] = stadnames_df['stadium']
# stadium_df.to_csv(path.join(DATA_DIR, 'data', 'stadiums.csv'), index=False, mode='w+')


#code to pull the daily batter stats vs that day's pitchers from baseball reference and save to a csv

# batter_pitcher_res = requests.get('https://stathead.com/baseball/batter_vs_pitcher.cgi?today=1', headers=HEADERS)

# batter_pitcher_soup = Soup(batter_pitcher_res.text)

# tables = batter_pitcher_soup.find_all('table')

# batter_pitcher_table = tables[0]

# rows = batter_pitcher_table.find_all('tr')

# first_data_row = rows[1]

# [str(x.string) for x in first_data_row.find_all('td')]

# list_of_parsed_rows = [parse_row(row) for row in rows[0:-1]]

# pvb_df = DataFrame(list_of_parsed_rows)
# pvb_df = pvb_df.dropna(how = 'all')
# pvb_df.columns = ["batter", "matchup", "pa", "ab", "h", "2b", "3b", "hr", "rbi", "bb", "so", "ba", "obp", "slg", "ops", "sh", "sf", "ibb", "hbp", "gdp", "view_pas"]
# pvb_df['batter'] = pvb_df['batter'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# pvb_df.to_csv(path.join(DATA_DIR, 'data', 'pvb.csv'), index=False, mode='w+')

#code to pull 2022 batting data and save to a csv file

batting_2022_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=c%2c4%2c6%2c5%2c7%2c11%2c45%2c47%2c23%2c38%2c40%2c305%2c308%2c311%2c-1%2c35%2c34%2c110%2c28%2c-1%2c21%2c22&season=2022&month=0&season1=2022&ind=0&team=&rost=&age=&filter=&players=&startdate=&enddate=&page=1_1000', headers = HEADERS)

batting_2022_soup = Soup(batting_2022_res.text)

tables2 = batting_2022_soup.find_all('table')

b22table = tables2[16]

rows2 = b22table.find_all('tr')

first_data_row2 = rows2[3]

[str(x.string) for x in first_data_row2.find_all('td')]

list_of_parsed_rows2 = [parse_row(row) for row in rows2[3:-1]]

bat22_df = DataFrame(list_of_parsed_rows2)
bat22_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "EV", "Barrel%", "HardHit%", "BB%", "K%", "SwStr%", "Pitches", "SB", "CS"]
bat22_df.to_csv(path.join(DATA_DIR, 'data', 'batting2022.csv'), index=False, mode='w+')

#code to pull batting data for previous 14 days and save to a csv file

batting_l_14_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=10&type=c,4,6,5,7,11,45,47,23,38,40,305,308,311,-1,35,34,110,28,-1,21,22&season=2022&month=2&season1=2022&ind=0&team=&rost=&age=0&filter=&players=&page=1_1000', headers = HEADERS)

batting_l_14_soup = Soup(batting_l_14_res.text)

tables4 = batting_l_14_soup.find_all('table')

bl14table = tables4[16]

rows4 = bl14table.find_all('tr')

first_data_row4 = rows4[3]

[str(x.string) for x in first_data_row4.find_all('td')]

list_of_parsed_rows4 = [parse_row(row) for row in rows4[3:-1]]

batL14_df = DataFrame(list_of_parsed_rows4)
batL14_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "EV", "Barrel%", "HardHit%", "BB%", "K%", "SwStr%", "Pitches", "SB", "CS"]
batL14_df.to_csv(path.join(DATA_DIR, 'data', 'battinglast14.csv'), index=False, mode='w+')

#code to pull batting data for previous 2 seasons vs Righties min.100PA and save to a csv file

batting_right_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=100&type=c%2c4%2c6%2c5%2c7%2c11%2c45%2c47%2c23%2c38%2c40%2c34%2c35&season=2022&month=14&season1=2021&ind=0&team=&rost=&age=0&filter=&players=&startdate=&enddate=&page=1_1000', headers = HEADERS)

batting_right_soup = Soup(batting_right_res.text)

tables6 = batting_right_soup.find_all('table')

batRttable = tables6[16]

rows6 = batRttable.find_all('tr')

first_data_row6 = rows6[3]

[str(x.string) for x in first_data_row6.find_all('td')]

list_of_parsed_rows6 = [parse_row(row) for row in rows6[3:-1]]

batRt_df = DataFrame(list_of_parsed_rows6)
batRt_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "BB%", "K%"]
batRt_df.to_csv(path.join(DATA_DIR, 'data', 'battingRighties.csv'), index=False, mode='w+')

#code to pull batting data for previous 2 seasons vs Lefties min.100PA and save to a csv file

batting_left_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=100&type=c,4,6,5,7,11,45,47,23,38,40,34,35&season=2022&month=13&season1=2021&ind=0&team=&rost=&age=0&filter=&players=&startdate=&enddate=&page=1_1000', headers = HEADERS)

batting_left_soup = Soup(batting_left_res.text)

tables7 = batting_left_soup.find_all('table')

batLttable = tables7[16]

rows7 = batLttable.find_all('tr')

first_data_row7 = rows7[3]

[str(x.string) for x in first_data_row7.find_all('td')]

list_of_parsed_rows7 = [parse_row(row) for row in rows7[3:-1]]

batLt_df = DataFrame(list_of_parsed_rows7)
batLt_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "BB%", "K%"]
batLt_df.to_csv(path.join(DATA_DIR, 'data', 'battingLefties.csv'), index=False, mode='w+')

#code to pull batting data for previous 2 seasons at Home min.100PA and save to a csv file

batting_home_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=100&type=c,4,6,5,7,11,45,47,23,38,40,34,35&season=2022&month=15&season1=2021&ind=0&team=&rost=&age=0&filter=&players=&startdate=&enddate=&page=1_1000', headers = HEADERS)

batting_home_soup = Soup(batting_home_res.text)

tables8 = batting_home_soup.find_all('table')

batHtable = tables8[16]

rows8 = batHtable.find_all('tr')

first_data_row8 = rows8[3]

[str(x.string) for x in first_data_row8.find_all('td')]

list_of_parsed_rows8 = [parse_row(row) for row in rows8[3:-1]]

batH_df = DataFrame(list_of_parsed_rows8)
batH_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "BB%", "K%"]
batH_df.to_csv(path.join(DATA_DIR, 'data', 'battingHome.csv'), index=False, mode='w+')

#code to pull batting data for previous 2 seasons Away min.100PA and save to a csv file

batting_away_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=100&type=c,4,6,5,7,11,45,47,23,38,40,34,35&season=2022&month=16&season1=2021&ind=0&team=&rost=&age=0&filter=&players=&startdate=&enddate=&page=1_1000', headers = HEADERS)

batting_away_soup = Soup(batting_away_res.text)

tables9 = batting_away_soup.find_all('table')

batAtable = tables9[16]

rows9 = batAtable.find_all('tr')

first_data_row9 = rows9[3]

[str(x.string) for x in first_data_row9.find_all('td')]

list_of_parsed_rows9 = [parse_row(row) for row in rows9[3:-1]]

batA_df = DataFrame(list_of_parsed_rows9)
batA_df.columns = ["rank", "Name", "Team", "G", "PA", "AB", "H", "HR", "FB%", "HR/FB", "AVG", "SLG", "ISO", "BB%", "K%"]
batA_df.to_csv(path.join(DATA_DIR, 'data', 'battingAway.csv'), index=False, mode='w+')

#code to pull 2021-22 pitching data and save to a csv file
pitching_2022_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=0&type=c,8,13,18,14,24,120,121,-1,31,110,113,330,331,-1,122,328,51,46,47,48,49,-1,45,322,325&season=2022&month=0&season1=2022&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page=1_500', headers = HEADERS)

pitching_2022_soup = Soup(pitching_2022_res.text)

tables5 = pitching_2022_soup.find_all('table')

p22table = tables5[16]

rows5 = p22table.find_all('tr')

first_data_row5 = rows5[3]

[str(x.string) for x in first_data_row5.find_all('td')]

list_of_parsed_rows5 = [parse_row(row) for row in rows5[3:-1]]

p22_df = DataFrame(list_of_parsed_rows5)
p22_df.columns = ["#", "Name", "Team", "GS", "IP", "HR", "TBF", "K", "K%", "BB%", "Pitches", "Contact%", "SwStr%", "CStr%", "CSW%", "SIERA", "HardHit%", "HR/FB", "GB/FB", "LD%", "GB%", "FB%", "FIP", "EV", "Barrel%"]
p22_df.to_csv(path.join(DATA_DIR, 'data', 'pitching2022.csv'), index=False, mode='w+')

#code to pull 2022 team bullpen data and save to a csv file
bullpen_2022_res = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=c%2c8%2c13%2c18%2c14%2c24%2c120%2c121%2c-1%2c31%2c110%2c113%2c330%2c331%2c-1%2c122%2c328%2c51%2c46%2c47%2c48%2c49&season=2022&month=0&season1=2022&ind=0&team=0%2cts&rost=0&age=0&filter=&players=0&startdate=&enddate=', headers = HEADERS)

bullpen_2022_soup = Soup(bullpen_2022_res.text)

tables10 = bullpen_2022_soup.find_all('table')

bp22table = tables10[16]

rows10 = bp22table.find_all('tr')

first_data_row10 = rows10[3]

[str(x.string) for x in first_data_row10.find_all('td')]

list_of_parsed_rows10 = [parse_row(row) for row in rows10[3:-1]]

bp22_df = DataFrame(list_of_parsed_rows10)
bp22_df.columns = ["#", "Team", "GS", "IP", "HR", "TBF", "K", "K%", "BB%", "Pitches", "Contact%", "SwStr%", "CStr%", "CSW%", "SIERA", "HardHit%", "HR/FB", "GB/FB", "LD%", "GB%", "FB%"]
bp22_df.to_csv(path.join(DATA_DIR, 'data', 'bullpen2022.csv'), index=False, mode='w+')