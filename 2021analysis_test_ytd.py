# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 19:28:18 2022

@author: graig
"""
import pandas as pd
import numpy as np
from os import path
from datetime import datetime, timedelta

DATA_DIR = '/Users/graig/Documents/BaseballBets'

#loads all 2022 pitch data that was filtered by 'last pitch of AB' to get the outcome of the atbat
dfAllData = pd.read_excel(
    path.join(DATA_DIR,'data','savant', '2022all.xlsx').replace("\\","/"))
#loads csv file with all team and stadium info
dfTeam = pd.read_csv(
    path.join(DATA_DIR,'data','savant', 'teamInfo.csv').replace("\\","/"))

#setting the dates for the time filtering
date = datetime(2022, 9, 26)
# n=10
# n1 = 21
# past_date = date - timedelta(days=n)
# past_date_sp = date - timedelta(days=n1)

#*****step 2: load data from csv files*****

#loads csv file with all 2022 hitters and their MLB id number
dfHit = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022hitters.csv').replace("\\","/"))
dfHitvLHP = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022hitters.csv').replace("\\","/"))
dfHitvRHP = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022hitters.csv').replace("\\","/"))

#loads csv file with all 2022 pitchers and their MLB id number
dfPit = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022pitchers.csv').replace("\\","/"))
dfPitvLHH = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022pitchers.csv').replace("\\","/"))
dfPitvRHH = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022pitchers.csv').replace("\\","/"))

#*****step 3: get game info for date*****

#get and merge in game info
games = dfAllData[['game_pk', 'game_date', 'home_team', 'away_team']]
games = games.loc[games['game_date'] == date]
games = games.drop_duplicates('game_pk')
games = pd.merge(games, dfTeam, left_on='home_team', right_on='ABR')
games.drop(['ABR', 'FG ABBR', 'Team'], axis=1, inplace=True) 

#to get  starting pitchers on date
dfStarters = dfAllData[['game_pk', 'game_date', 'home_team', 'away_team', 'inning', 'inning_topbot', 'pitcher', 'p_throws']] #filter for sp info
dfStarters = dfStarters.loc[dfStarters['game_date'] == date]
dfStarters = dfStarters.loc[dfStarters['inning'] == 1] #grab only pitchers from 1st inning
dfHomeStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Top'] #grab home pitchers from top of 1st
dfHomeStart['sort'] = dfHomeStart['pitcher'].astype(str) + dfHomeStart['game_pk'].astype(str) #create a helper column adding pitcher id to game id to remove duplicates
dfHomeStart = dfHomeStart.drop_duplicates(subset=['sort']) #drop duplicate
dfHomeStart = dfHomeStart[['game_pk', 'away_team', 'pitcher', 'p_throws']] #get rid of unneeded columns
dfHomeStart.rename(columns={'pitcher': 'starter_id', 'away_team': 'team'}, inplace=True) #rename for merging
dfHomeStart = pd.merge(dfHomeStart, dfPit, left_on='starter_id', right_on='player_id') #merge pitcher names in
dfHomeStart.rename(columns={'player_name': 'starter', 'p_throws':'T'}, inplace=True) #rename pitcher columns for home teams
dfHomeStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
# dfHomeStart.to_csv(path.join(DATA_DIR, 'data', 'testing', 'hometeamSP.csv'), index=False, mode='w+')
dfAwayStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Bot'] #all this is the same but for the away starter
dfAwayStart['sort'] = dfAwayStart['pitcher'].astype(str) + dfAwayStart['game_pk'].astype(str)
dfAwayStart = dfAwayStart.drop_duplicates(subset=['sort'])
dfAwayStart = dfAwayStart[['game_pk', 'home_team', 'pitcher', 'p_throws']]
dfAwayStart.rename(columns={'pitcher': 'starter_id', 'home_team': 'team'}, inplace=True)
dfAwayStart = pd.merge(dfAwayStart, dfPit, left_on='starter_id', right_on='player_id')
dfAwayStart.rename(columns={'player_name': 'starter', 'p_throws':'T'}, inplace=True) #rename pitcher columns for home teams
dfAwayStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
dailyStarters = dfHomeStart.append(dfAwayStart, ignore_index=True)
games = pd.merge(games, dailyStarters, on='game_pk')
games = games.drop_duplicates(subset=['starter_id'])
#delete the starter tables
del dailyStarters
del dfAwayStart
del dfHomeStart
del dfStarters

#to get previous lineups
dfLineups = dfAllData[['game_date', 'home_team', 'away_team', 'at_bat_number', 'inning', 'inning_topbot', 'batter', 'stand', 'pitcher', 'game_pk']]
dfLineups = dfLineups.loc[dfLineups['game_date'] == date]
dfLineups = dfLineups.loc[dfLineups['inning'] <= 3]
dfHomeLineup = dfLineups.loc[dfLineups['inning_topbot'] == 'Bot']
dfHomeLineup = dfHomeLineup.sort_values(by=['game_date', 'home_team', 'at_bat_number'], ascending=True)
dfHomeLineup['sort'] = dfHomeLineup['batter'].astype(str) + dfHomeLineup['game_date'].astype(str)
dfHomeLineup = dfHomeLineup.drop_duplicates(subset=['sort'])
dfHomeLineup.rename(columns={'home_team': 'team'}, inplace=True)
dfStartingLineup = dfHomeLineup[['game_pk', 'game_date', 'team', 'batter', 'stand']]

dfAwayLineup = dfLineups.loc[dfLineups['inning_topbot'] == 'Top']
dfAwayLineup = dfAwayLineup.sort_values(by=['game_date', 'away_team', 'at_bat_number'], ascending=True)
dfAwayLineup['sort'] = dfAwayLineup['batter'].astype(str) + dfAwayLineup['game_date'].astype(str)
dfAwayLineup = dfAwayLineup.drop_duplicates(subset=['sort'])
dfAwayLineup.rename(columns={'away_team': 'team'}, inplace=True)
dfStartingLineup2 = dfAwayLineup[['game_pk', 'game_date', 'team', 'batter', 'stand']]
#merge home and away lineups to one file
frames = [dfStartingLineup, dfStartingLineup2]
lineups = pd.concat(frames)

lineups = pd.merge(lineups, games, left_on=['game_pk', 'game_date', 'team'], right_on=['game_pk','game_date','team'])
del dfHomeLineup
del dfAwayLineup
del dfStartingLineup
del dfStartingLineup2

lineups_v_LHP = lineups.loc[lineups['T'] == 'L']
lineups_v_RHP = lineups.loc[lineups['T'] == 'R']
pitchers_vLHH = lineups.loc[lineups['stand'] == 'L']
pitchers_vRHH = lineups.loc[lineups['stand'] == 'R']

#narrows the event data to get to relevant columns and simplify the data
dfTestData = dfAllData.loc[(dfAllData['game_date'] < date)]
# dfRecentData = dfTestData.loc[(dfTestData['game_date'] >= past_date)]
# dfRecentData_SP = dfTestData.loc[(dfTestData['game_date'] >= past_date_sp)]
dfGameResult = dfAllData.loc[(dfAllData['game_date'] == date)]
dfTrimData = dfTestData[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
# dfRecentTrim = dfRecentData[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
# dfRecentTrimSP = dfRecentData_SP[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws','type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
batting_vs_lhp = dfTrimData.loc[dfTrimData['p_throws'] == 'L']
batting_vs_rhp = dfTrimData.loc[dfTrimData['p_throws'] == 'R']
pitching_vs_lhh = dfTrimData.loc[dfTrimData['stand'] == 'L']
pitching_vs_rhh = dfTrimData.loc[dfTrimData['stand'] == 'R']

dfGameResult['Act-HR'] = dfGameResult['events'] == 'home_run'

sum_columns = ['Act-HR']
game_result = dfGameResult.groupby(['game_pk', 'batter']).sum()[sum_columns]
lineups = pd.merge(lineups, game_result, on=['game_pk', 'batter'])

#***ASSEMBLING BATTER DATA***
#this is for overall batted ball data summarized by batter
dfHit['PA'] = dfHit['player_id'].map(dfTrimData['batter'].value_counts())
is_ball_in_play = dfTrimData.loc[dfTrimData['type'] == 'X']
is_fly_ball = dfTrimData.loc[dfTrimData['bb_type'] == 'fly_ball']
is_home_run = dfTrimData.loc[dfTrimData['events'] == 'home_run']
is_hardhit_FB = dfTrimData.loc[(dfTrimData['launch_angle'] >= 23) & (dfTrimData['launch_speed'] >= 94.5)]
is_hardhit_HR = dfTrimData.loc[(dfTrimData['launch_angle'] >= 23) & (dfTrimData['launch_speed'] >= 94.5) & (dfTrimData['events'] == 'home_run')]
is_strikeout = dfTrimData.loc[dfTrimData['events'] == 'strikeout']
df80thPctEV = is_ball_in_play.groupby('batter')['launch_speed'].quantile(0.80)
dfHit['BIP'] = dfHit['player_id'].map(is_ball_in_play['batter'].value_counts())
dfHit = dfHit.merge((is_ball_in_play.groupby(['batter']).mean()), left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_angle': 'LA-OVR', 'launch_speed': 'EV-Ovr'}, inplace=True)
dfHit['FB'] = dfHit['player_id'].map(is_fly_ball['batter'].value_counts())
dfHit['HR'] = dfHit['player_id'].map(is_home_run['batter'].value_counts())
dfHit['K'] = dfHit['player_id'].map(is_strikeout['batter'].value_counts())
dfHit['K%'] = dfHit['K'] / dfHit['PA']
dfHit['HR/BIP'] = dfHit['HR'] / dfHit['BIP']
dfHit['HH FB'] = dfHit['player_id'].map(is_hardhit_FB['batter'].value_counts())
dfHit['HH HR'] = dfHit['player_id'].map(is_hardhit_HR['batter'].value_counts())
dfHit['PA/HR'] = dfHit['PA'] / dfHit['HR']
dfHit['FB%'] = dfHit['FB'] / dfHit['BIP']
dfHit['HHFB%'] = dfHit['HH FB'] / dfHit['BIP']
dfHit = dfHit.merge(df80thPctEV, left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_speed': '80thPctEV-OVR'}, inplace=True)
dfHit.drop(['pitcher','game_pk', 'K', 'FB', 'BIP', 'HH FB', 'HH HR'], axis=1, inplace=True)

#get recent X days of stats
# dfHit['PA-L10'] = dfHit['player_id'].map(dfRecentData['batter'].value_counts())
# is_ball_in_play_l10 = dfRecentTrim.loc[dfRecentTrim['type'] == 'X']
# is_fly_ball_l10 = dfRecentTrim.loc[dfRecentTrim['bb_type'] == 'fly_ball']
# is_home_run_l10 = dfRecentTrim.loc[dfRecentTrim['events'] == 'home_run']
# is_hardhit_FB_l10 = dfRecentTrim.loc[(dfRecentTrim['launch_angle'] >= 23) & (dfRecentTrim['launch_speed'] >= 94.5)]
# is_hardhit_HR_l10 = dfRecentTrim.loc[(dfRecentTrim['launch_angle'] >= 23) & (dfRecentTrim['launch_speed'] >= 94.5) & (dfRecentTrim['events'] == 'home_run')]
# is_strikeout_l10 = dfRecentTrim.loc[dfTrimData['events'] == 'strikeout']
# df80thPctEV_l10 = is_ball_in_play_l10.groupby('batter')['launch_speed'].quantile(0.80)
# dfHit['BIP-L10'] = dfHit['player_id'].map(is_ball_in_play_l10['batter'].value_counts())
# dfHit = dfHit.merge((is_ball_in_play_l10.groupby(['batter']).mean()), left_on='player_id', right_on='batter')
# dfHit.rename(columns={'launch_angle': 'LA-L10', 'launch_speed': 'EV-L10'}, inplace=True)
# dfHit['FB-L10'] = dfHit['player_id'].map(is_fly_ball_l10['batter'].value_counts())
# dfHit['HR-L10'] = dfHit['player_id'].map(is_home_run_l10['batter'].value_counts())
# dfHit['K-L10'] = dfHit['player_id'].map(is_strikeout_l10['batter'].value_counts())
# dfHit['K%-L10'] = dfHit['K-L10'] / dfHit['PA-L10']
# dfHit['HR/BIP-L10'] = dfHit['HR-L10'] / dfHit['BIP-L10']
# dfHit['HH FB-L10'] = dfHit['player_id'].map(is_hardhit_FB_l10['batter'].value_counts())
# dfHit['HH HR-L10'] = dfHit['player_id'].map(is_hardhit_HR_l10['batter'].value_counts())
# dfHit['PA/HR-L10'] = dfHit['PA-L10'] / dfHit['HR-L10']
# dfHit['FB%-L10'] = dfHit['FB-L10'] / dfHit['BIP-L10']
# dfHit['HHFB%-L10'] = dfHit['HH FB-L10'] / dfHit['BIP-L10']
# dfHit = dfHit.merge(df80thPctEV_l10, left_on='player_id', right_on='batter')
# dfHit.rename(columns={'launch_speed': '80thPctEV-L10'}, inplace=True)
# dfHit.drop(['pitcher','game_pk', 'BIP-L10', 'FB-L10', 'K-L10', 'HH FB-L10', 'HH HR-L10'], axis=1, inplace=True)

#merge ytd and recent stats into lineup database
lineups = pd.merge(lineups, dfHit, left_on='batter', right_on='player_id')
del dfHit

#filtered for plate appearances vs left-handed pitchers
dfHitvLHP['PA-vPH'] = dfHitvLHP['player_id'].map(batting_vs_lhp['batter'].value_counts())
is_ball_in_play_vLHP = batting_vs_lhp.loc[batting_vs_lhp['type'] == 'X']
is_fly_ball_vLHP = batting_vs_lhp.loc[batting_vs_lhp['bb_type'] == 'fly_ball']
is_home_run_vLHP = batting_vs_lhp.loc[batting_vs_lhp['events'] == 'home_run']
is_hardhit_FB_vLHP = batting_vs_lhp.loc[(batting_vs_lhp['launch_angle'] >= 23) & (batting_vs_lhp['launch_speed'] >= 94.5)]
is_hardhit_HR_vLHP = batting_vs_lhp.loc[(batting_vs_lhp['launch_angle'] >= 23) & (batting_vs_lhp['launch_speed'] >= 94.5) & (batting_vs_lhp['events'] == 'home_run')]
df80thPctEV_vLHP = is_ball_in_play_vLHP.groupby('batter')['launch_speed'].quantile(0.80)
is_strikeout_vLHP = batting_vs_lhp.loc[batting_vs_lhp['events'] == 'strikeout']
dfHitvLHP['BIP-vPH'] = dfHitvLHP['player_id'].map(is_ball_in_play_vLHP['batter'].value_counts())
dfHitvLHP.rename(columns={'launch_angle': 'LA-vPH', 'launch_speed': 'EV-vPH', 'player_id': 'batter'}, inplace=True)
dfHitvLHP['K-vPH'] = dfHitvLHP['batter'].map(is_strikeout_vLHP['batter'].value_counts())
dfHitvLHP['FB-vPH'] = dfHitvLHP['batter'].map(is_fly_ball_vLHP['batter'].value_counts())
dfHitvLHP['HR-vPH'] = dfHitvLHP['batter'].map(is_home_run_vLHP['batter'].value_counts())
dfHitvLHP['K%-vPH'] = dfHitvLHP['K-vPH'] / dfHitvLHP['PA-vPH']
dfHitvLHP['HH FB-vPH'] = dfHitvLHP['batter'].map(is_hardhit_FB_vLHP['batter'].value_counts())
dfHitvLHP['HH HR-vPH'] = dfHitvLHP['batter'].map(is_hardhit_HR_vLHP['batter'].value_counts())
dfHitvLHP['PA/HR-vPH'] = dfHitvLHP['PA-vPH'] / dfHitvLHP['HR-vPH']
dfHitvLHP['FB%-vPH'] = dfHitvLHP['FB-vPH'] / dfHitvLHP['BIP-vPH']
dfHitvLHP['HHFB%-vPH'] = dfHitvLHP['HH FB-vPH'] / dfHitvLHP['BIP-vPH']
dfHitvLHP = dfHitvLHP.merge(df80thPctEV_vLHP, on='batter')
dfHitvLHP.rename(columns={'launch_speed': '80thPctEV-vPH'}, inplace=True)
dfHitvLHP.drop(['player_name', 'BIP-vPH', 'FB-vPH', 'HH FB-vPH', 'HH HR-vPH', 'K-vPH'], axis=1, inplace=True)
# dfHit = dfHit.merge(df80thPctEV_vPH, left_on='player_id', right_on='batter')
lineups_v_LHP = pd.merge(lineups_v_LHP, dfHitvLHP, on='batter')
del dfHitvLHP

#filtered for plate appearances vs right-handed pitchers
dfHitvRHP['PA-vPH'] = dfHitvRHP['player_id'].map(batting_vs_rhp['batter'].value_counts())
is_ball_in_play_vRHP = batting_vs_rhp.loc[batting_vs_rhp['type'] == 'X']
is_fly_ball_vRHP = batting_vs_rhp.loc[batting_vs_rhp['bb_type'] == 'fly_ball']
is_home_run_vRHP = batting_vs_rhp.loc[batting_vs_rhp['events'] == 'home_run']
is_hardhit_FB_vRHP = batting_vs_rhp.loc[(batting_vs_rhp['launch_angle'] >= 23) & (batting_vs_rhp['launch_speed'] >= 94.5)]
is_hardhit_HR_vRHP = batting_vs_rhp.loc[(batting_vs_rhp['launch_angle'] >= 23) & (batting_vs_rhp['launch_speed'] >= 94.5) & (batting_vs_rhp['events'] == 'home_run')]
df80thPctEV_vRHP = is_ball_in_play_vRHP.groupby('batter')['launch_speed'].quantile(0.80)
is_strikeout_vRHP = batting_vs_rhp.loc[batting_vs_rhp['events'] == 'strikeout']
dfHitvRHP['BIP-vPH'] = dfHitvRHP['player_id'].map(is_ball_in_play_vRHP['batter'].value_counts())
dfHitvRHP.rename(columns={'launch_angle': 'LA-vPH', 'launch_speed': 'EV-vPH', 'player_id': 'batter'}, inplace=True)
dfHitvRHP['K-vPH'] = dfHitvRHP['batter'].map(is_strikeout_vRHP['batter'].value_counts())
dfHitvRHP['FB-vPH'] = dfHitvRHP['batter'].map(is_fly_ball_vRHP['batter'].value_counts())
dfHitvRHP['HR-vPH'] = dfHitvRHP['batter'].map(is_home_run_vRHP['batter'].value_counts())
dfHitvRHP['K%-vPH'] = dfHitvRHP['K-vPH'] / dfHitvRHP['PA-vPH']
dfHitvRHP['HH FB-vPH'] = dfHitvRHP['batter'].map(is_hardhit_FB_vRHP['batter'].value_counts())
dfHitvRHP['HH HR-vPH'] = dfHitvRHP['batter'].map(is_hardhit_HR_vRHP['batter'].value_counts())
dfHitvRHP['PA/HR-vPH'] = dfHitvRHP['PA-vPH'] / dfHitvRHP['HR-vPH']
dfHitvRHP['FB%-vPH'] = dfHitvRHP['FB-vPH'] / dfHitvRHP['BIP-vPH']
dfHitvRHP['HHFB%-vPH'] = dfHitvRHP['HH FB-vPH'] / dfHitvRHP['BIP-vPH']
dfHitvRHP = dfHitvRHP.merge(df80thPctEV_vRHP, on='batter')
dfHitvRHP.rename(columns={'launch_speed': '80thPctEV-vPH'}, inplace=True)
dfHitvRHP.drop(['player_name', 'BIP-vPH', 'FB-vPH', 'HH FB-vPH', 'HH HR-vPH', 'K-vPH'], axis=1, inplace=True)
# dfHit = dfHit.merge(df80thPctEV_vPH, left_on='player_id', right_on='batter')
lineups_v_RHP = pd.merge(lineups_v_RHP, dfHitvRHP, on='batter')
del dfHitvRHP

lineup_splits = lineups_v_RHP.append(lineups_v_LHP, ignore_index=True)
lineup_splits.drop(['game_date', 'team', 'stand', 'home_team', 'away_team', 'Park', 'Righties', 'Lefties', 'starter_id', 'T', 'starter'], axis=1, inplace=True)

lineups = pd.merge(lineups, lineup_splits, on=['game_pk', 'batter'])
lineups.rename(columns={'player_name': 'hitter_name'}, inplace=True)
lineups.drop('player_id', axis=1, inplace=True)
del lineups_v_LHP
del lineups_v_RHP
del lineup_splits


#***ASSEMBLING PITCHER DATA***
#adds column for total batters faced (TBF)
dfPit['TBF'] = dfPit['player_id'].map(dfTrimData['pitcher'].value_counts())
is_ball_in_play_pit = dfTrimData.loc[dfTrimData['type'] == 'X']
is_fly_ball_pit = dfTrimData.loc[dfTrimData['bb_type'] == 'fly_ball']
is_home_run_pit = dfTrimData.loc[dfTrimData['events'] == 'home_run']
is_hardhit_FB_pit = dfTrimData.loc[(dfTrimData['launch_angle'] >= 23) & (dfTrimData['launch_speed'] >= 94.5)]
is_hardhit_HR_pit = dfTrimData.loc[(dfTrimData['launch_angle'] >= 23) & (dfTrimData['launch_speed'] >= 94.5) & (dfTrimData['events'] == 'home_run')]
df80thPctEV_pit = is_ball_in_play_pit.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP_sp'] = dfPit['player_id'].map(is_ball_in_play_pit['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_pit.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-OVR_sp', 'launch_speed': 'EV-OVR_sp'}, inplace=True)
dfPit['K_sp'] = dfPit['player_id'].map(is_strikeout['pitcher'].value_counts())
dfPit['FB_sp'] = dfPit['player_id'].map(is_fly_ball_pit['pitcher'].value_counts())
dfPit['HR_sp'] = dfPit['player_id'].map(is_home_run_pit['pitcher'].value_counts())
dfPit['K%_sp'] = dfPit['K_sp'] / dfPit['TBF']
dfPit['HH FB_sp'] = dfPit['player_id'].map(is_hardhit_FB_pit['pitcher'].value_counts())
dfPit['HH HR_sp'] = dfPit['player_id'].map(is_hardhit_HR_pit['pitcher'].value_counts())
dfPit['TBF/HR_sp'] = dfPit['TBF'] / dfPit['HR_sp']
dfPit['FB%_sp'] = dfPit['FB_sp'] / dfPit['BIP_sp']
dfPit['HHFB%_sp'] = dfPit['HH FB_sp'] / dfPit['BIP_sp']
dfPit = dfPit.merge(df80thPctEV_pit, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-sp'}, inplace=True)
dfPit.drop(['batter','game_pk', 'FB_sp', 'HH FB_sp', 'HH HR_sp'], axis=1, inplace=True)

# dfPit['TBF-L21'] = dfPit['player_id'].map(dfRecentTrimSP['pitcher'].value_counts())
# is_ball_in_play_pit_l21 = dfRecentTrimSP.loc[dfRecentTrimSP['type'] == 'X']
# is_fly_ball_pit_l21 = dfRecentTrimSP.loc[dfRecentTrimSP['bb_type'] == 'fly_ball']
# is_home_run_pit_l21 = dfRecentTrimSP.loc[dfRecentTrimSP['events'] == 'home_run']
# is_hardhit_FB_pit_l21 = dfRecentTrimSP.loc[(dfRecentTrimSP['launch_angle'] >= 23) & (dfRecentTrimSP['launch_speed'] >= 94.5)]
# is_hardhit_HR_pit_l21 = dfRecentTrimSP.loc[(dfRecentTrimSP['launch_angle'] >= 23) & (dfRecentTrimSP['launch_speed'] >= 94.5) & (dfRecentTrimSP['events'] == 'home_run')]
# is_strikeout_l21 = dfRecentTrimSP.loc[dfRecentTrimSP['events'] == 'strikeout']
# df80thPctEV_pit_l21 = is_ball_in_play_pit_l21.groupby('pitcher')['launch_speed'].quantile(0.80)
# dfPit['BIP-L21'] = dfPit['player_id'].map(is_ball_in_play_pit_l21['pitcher'].value_counts())
# dfPit = dfPit.merge((is_ball_in_play_pit_l21.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
# dfPit.rename(columns={'launch_angle': 'LA-L21', 'launch_speed': 'EV-L21'}, inplace=True)
# dfPit['K-L21'] = dfPit['player_id'].map(is_strikeout_l21['pitcher'].value_counts())
# dfPit['FB-L21'] = dfPit['player_id'].map(is_fly_ball_pit_l21['pitcher'].value_counts())
# dfPit['HR-L21'] = dfPit['player_id'].map(is_home_run_pit_l21['pitcher'].value_counts())
# dfPit['K%-L21'] = dfPit['K-L21'] / dfPit['TBF-L21']
# dfPit['HH FB-L21'] = dfPit['player_id'].map(is_hardhit_FB_pit_l21['pitcher'].value_counts())
# dfPit['HH HR-L21'] = dfPit['player_id'].map(is_hardhit_HR_pit_l21['pitcher'].value_counts())
# dfPit['TBF/HR-L21'] = dfPit['TBF-L21'] / dfPit['HR-L21']
# dfPit['FB%-L21'] = dfPit['FB-L21'] / dfPit['BIP-L21']
# dfPit['HHFB%-L21'] = dfPit['HH FB-L21'] / dfPit['BIP-L21']
# dfPit = dfPit.merge(df80thPctEV_pit_l21, left_on='player_id', right_on='pitcher')
# dfPit.rename(columns={'launch_speed': '80thPctEV-L21'}, inplace=True)
# dfPit.drop(['batter','game_pk', 'player_name'], axis=1, inplace=True)

lineups = pd.merge(lineups, dfPit, left_on='starter_id', right_on='player_id')
del dfPit


#filtered for plate appearances vs left-handed batters
dfPitvLHH['TBF-vBH'] = dfPitvLHH['player_id'].map(pitching_vs_lhh['pitcher'].value_counts())
is_ball_in_play_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['type'] == 'X']
is_fly_ball_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['bb_type'] == 'fly_ball']
is_home_run_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['events'] == 'home_run']
is_hardhit_FB_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['launch_angle'] >= 23) & (pitching_vs_lhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['launch_angle'] >= 23) & (pitching_vs_lhh['launch_speed'] >= 94.5) & (pitching_vs_lhh['events'] == 'home_run')]
is_strikeout_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['events'] == 'strikeout']
df80thPctEV_vLHH = is_ball_in_play_vLHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPitvLHH['BIP-vBH'] = dfPitvLHH['player_id'].map(is_ball_in_play_vLHH['pitcher'].value_counts())
dfPitvLHH = dfPitvLHH.merge((is_ball_in_play_vLHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPitvLHH.rename(columns={'launch_angle': 'LA-vBH', 'launch_speed': 'EV-vBH'}, inplace=True)
dfPitvLHH['K-vBH'] = dfPitvLHH['player_id'].map(is_strikeout_vLHH['pitcher'].value_counts())
dfPitvLHH['FB-vBH'] = dfPitvLHH['player_id'].map(is_fly_ball_vLHH['pitcher'].value_counts())
dfPitvLHH['HR-vBH'] = dfPitvLHH['player_id'].map(is_home_run_vLHH['pitcher'].value_counts())
dfPitvLHH['K%-vBH'] = dfPitvLHH['K-vBH'] / dfPitvLHH['TBF-vBH']
dfPitvLHH['HH FB-vBH'] = dfPitvLHH['player_id'].map(is_hardhit_FB_vLHH['pitcher'].value_counts())
dfPitvLHH['HH HR-vBH'] = dfPitvLHH['player_id'].map(is_hardhit_HR_vLHH['pitcher'].value_counts())
dfPitvLHH['TBF/HR-vBH'] = dfPitvLHH['TBF-vBH'] / dfPitvLHH['HR-vBH']
dfPitvLHH['FB%-vBH'] = dfPitvLHH['FB-vBH'] / dfPitvLHH['BIP-vBH']
dfPitvLHH['HHFB%-vBH'] = dfPitvLHH['HH FB-vBH'] / dfPitvLHH['BIP-vBH']
dfPitvLHH = dfPitvLHH.merge(df80thPctEV_vLHH, left_on='player_id', right_on='pitcher')
dfPitvLHH.rename(columns={'launch_speed': '80thPctEV-vBH'}, inplace=True)
dfPitvLHH.drop(['player_name', 'batter', 'BIP-vBH', 'K-vBH', 'FB-vBH', 'HH FB-vBH', 'HH HR-vBH','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs right-handed batters
dfPitvRHH['TBF-vBH'] = dfPitvRHH['player_id'].map(pitching_vs_rhh['pitcher'].value_counts())
is_ball_in_play_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['type'] == 'X']
is_fly_ball_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['bb_type'] == 'fly_ball']
is_home_run_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['events'] == 'home_run']
is_hardhit_FB_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['launch_angle'] >= 23) & (pitching_vs_rhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['launch_angle'] >= 23) & (pitching_vs_rhh['launch_speed'] >= 94.5) & (pitching_vs_rhh['events'] == 'home_run')]
is_strikeout_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['events'] == 'strikeout']
df80thPctEV_vRHH = is_ball_in_play_vRHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPitvRHH['BIP-vBH'] = dfPitvRHH['player_id'].map(is_ball_in_play_vRHH['pitcher'].value_counts())
dfPitvRHH = dfPitvRHH.merge((is_ball_in_play_vRHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPitvRHH.rename(columns={'launch_angle': 'LA-vBH', 'launch_speed': 'EV-vBH'}, inplace=True)
dfPitvRHH['K-vBH'] = dfPitvRHH['player_id'].map(is_strikeout_vRHH['pitcher'].value_counts())
dfPitvRHH['FB-vBH'] = dfPitvRHH['player_id'].map(is_fly_ball_vRHH['pitcher'].value_counts())
dfPitvRHH['HR-vBH'] = dfPitvRHH['player_id'].map(is_home_run_vRHH['pitcher'].value_counts())
dfPitvRHH['K%-vBH'] = dfPitvRHH['K-vBH'] / dfPitvRHH['TBF-vBH']
dfPitvRHH['HH FB-vBH'] = dfPitvRHH['player_id'].map(is_hardhit_FB_vRHH['pitcher'].value_counts())
dfPitvRHH['HH HR-vBH'] = dfPitvRHH['player_id'].map(is_hardhit_HR_vRHH['pitcher'].value_counts())
dfPitvRHH['TBF/HR-vBH'] = dfPitvRHH['TBF-vBH'] / dfPitvRHH['HR-vBH']
dfPitvRHH['FB%-vBH'] = dfPitvRHH['FB-vBH'] / dfPitvRHH['BIP-vBH']
dfPitvRHH['HHFB%-vBH'] = dfPitvRHH['HH FB-vBH'] / dfPitvRHH['BIP-vBH']
dfPitvRHH = dfPitvRHH.merge(df80thPctEV_vRHH, left_on='player_id', right_on='pitcher')
dfPitvRHH.rename(columns={'launch_speed': '80thPctEV-vBH'}, inplace=True)
dfPitvRHH.drop(['player_name', 'batter', 'BIP-vBH', 'K-vBH', 'FB-vBH', 'HH FB-vBH', 'HH HR-vBH','game_pk'], axis=1, inplace=True)

pitchers_vLHH = pd.merge(pitchers_vLHH, dfPitvLHH, left_on='starter_id', right_on='player_id')
pitchers_vRHH = pd.merge(pitchers_vRHH, dfPitvRHH, left_on='starter_id', right_on='player_id')
del dfPitvLHH
del dfPitvRHH

pitcher_splits = pitchers_vLHH.append(pitchers_vRHH, ignore_index=True)
pitcher_splits.drop(['game_pk','game_date', 'team', 'batter', 'stand', 'home_team',
       'away_team', 'Park', 'Righties', 'Lefties','T',
       'starter', 'player_id'], axis=1, inplace=True)
lineups = pd.merge(lineups, pitcher_splits, on='starter_id')

lineups_parkfactorLHH = lineups.loc[lineups['stand'] == 'L']
lineups_parkfactorLHH.drop(['Righties'], axis=1, inplace=True)
lineups_parkfactorLHH.rename(columns={'Lefties': 'PFx'}, inplace=True)

lineups_parkfactorRHH = lineups.loc[lineups['stand'] == 'R']
lineups_parkfactorRHH.drop(['Lefties'], axis=1, inplace=True)
lineups_parkfactorRHH.rename(columns={'Righties': 'PFx'}, inplace=True)


lineups = lineups_parkfactorLHH.append(lineups_parkfactorRHH, ignore_index=True)
lineups = lineups.drop_duplicates(subset=['batter'])
del lineups_parkfactorLHH
del lineups_parkfactorRHH
del dfTestData
# del dfRecentData
# del dfRecentData_SP
del dfGameResult
del dfTrimData
# del dfRecentTrim
# del dfRecentTrimSP
del batting_vs_lhp
del batting_vs_rhp
del pitching_vs_lhh
del pitching_vs_rhh

# analysis_table = lineups

analysis_table = analysis_table.append(lineups, ignore_index=True) 

analysis_table.to_csv(path.join(DATA_DIR, 'data', 'testing', 'update.csv'), index=False, mode='w+')
