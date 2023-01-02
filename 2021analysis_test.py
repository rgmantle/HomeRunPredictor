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

#setting the dates for the time filtering
date = datetime(2022, 7,11)
n=10
n1 = 21
past_date = date - timedelta(days=n)
past_date_sp = date - timedelta(days=n1)


#loads csv file with all 2022 hitters and their MLB id number
dfHit = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022hitters.csv').replace("\\","/"))

#loads csv file with all 2022 pitchers and their MLB id number
dfPit = pd.read_csv(
    path.join(DATA_DIR,'data','savant', '2022pitchers.csv').replace("\\","/"))

#loads csv file with all team and stadium info
dfTeam = pd.read_csv(
    path.join(DATA_DIR,'data','savant', 'teamInfo.csv').replace("\\","/"))

#loads all 2022 pitch data that was filtered by 'last pitch of AB' to get the outcome of the atbat
dfAllData = pd.read_excel(
    path.join(DATA_DIR,'data','savant', '2022all.xlsx').replace("\\","/"))

#get and merge in game info
games = dfAllData[['game_pk', 'game_date', 'home_team', 'away_team']]
games = games.drop_duplicates('game_pk')
games = pd.merge(games, dfTeam, left_on='home_team', right_on='ABR')
games.drop(['ABR', 'FG ABBR', 'Team'], axis=1, inplace=True) 

#to get previous starting pitchers
dfStarters = dfAllData[['game_pk','inning', 'inning_topbot', 'pitcher']] #filter for sp info
dfStarters = dfStarters.loc[dfStarters['inning'] == 1] #grab only pitchers from 1st inning
dfHomeStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Top'] #grab home pitchers from top of 1st
dfHomeStart['sort'] = dfHomeStart['pitcher'].astype(str) + dfHomeStart['game_pk'].astype(str) #create a helper column adding pitcher id to game id to remove duplicates
dfHomeStart = dfHomeStart.drop_duplicates(subset=['sort']) #drop duplicate
dfHomeStart = dfHomeStart[['game_pk', 'pitcher']] #get rid of unneeded columns
dfHomeStart.rename(columns={'pitcher': 'home_starter_id'}, inplace=True) #rename for merging
dfHomeStart = pd.merge(dfHomeStart, dfPit, left_on='home_starter_id', right_on='player_id') #merge pitcher names in
dfHomeStart.rename(columns={'player_name': 'home_sp'}, inplace=True) #rename pitcher columns for home teams
dfHomeStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
# dfHomeStart.to_csv(path.join(DATA_DIR, 'data', 'testing', 'hometeamSP.csv'), index=False, mode='w+')
dfAwayStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Bot'] #all this is the same but for the away starter
dfAwayStart['sort'] = dfAwayStart['pitcher'].astype(str) + dfAwayStart['game_pk'].astype(str)
dfAwayStart = dfAwayStart.drop_duplicates(subset=['sort'])
dfAwayStart = dfAwayStart[['game_pk', 'pitcher']]
dfAwayStart.rename(columns={'pitcher': 'away_starter_id'}, inplace=True)
dfAwayStart = pd.merge(dfAwayStart, dfPit, left_on='away_starter_id', right_on='player_id')
dfAwayStart.rename(columns={'player_name': 'away_sp'}, inplace=True) #rename pitcher columns for home teams
dfAwayStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
dailyStarters = pd.merge(dfHomeStart, dfAwayStart, on='game_pk')
games = pd.merge(games, dailyStarters, on='game_pk')

games.to_csv(path.join(DATA_DIR, 'data', 'testing', 'games2022.csv'), index=False, mode='w+')
#delete the starter tables
del dailyStarters
del dfAwayStart
del dfHomeStart
del dfStarters

#to get previous lineups
dfLineups = dfAllData[['game_date', 'home_team', 'away_team', 'at_bat_number', 'inning', 'inning_topbot', 'batter', 'pitcher', 'game_pk']]
dfLineups = dfLineups.loc[dfLineups['inning'] <= 3]
dfHomeLineup = dfLineups.loc[dfLineups['inning_topbot'] == 'Bot']
dfHomeLineup = dfHomeLineup.sort_values(by=['game_date', 'home_team', 'at_bat_number'], ascending=True)
dfHomeLineup['sort'] = dfHomeLineup['batter'].astype(str) + dfHomeLineup['game_date'].astype(str)
dfHomeLineup = dfHomeLineup.drop_duplicates(subset=['sort'])
del dfHomeLineup['away_team']
dfHomeLineup.rename(columns={'home_team': 'team'}, inplace=True)
dfStartingLineup = dfHomeLineup[['game_pk', 'game_date', 'team', 'batter']]

dfAwayLineup = dfLineups.loc[dfLineups['inning_topbot'] == 'Top']
dfAwayLineup = dfAwayLineup.sort_values(by=['game_date', 'away_team', 'at_bat_number'], ascending=True)
dfAwayLineup['sort'] = dfAwayLineup['batter'].astype(str) + dfAwayLineup['game_date'].astype(str)
dfAwayLineup = dfAwayLineup.drop_duplicates(subset=['sort'])
dfAwayLineup.rename(columns={'away_team': 'team'}, inplace=True)
dfStartingLineup2 = dfAwayLineup[['game_pk', 'game_date', 'team', 'batter']]
#merge home and away lineups to one file
frames = [dfStartingLineup, dfStartingLineup2]
lineups = pd.concat(frames)

lineups.to_csv(path.join(DATA_DIR, 'data', 'testing', 'lineups2022.csv'), index=False, mode='w+')

lineup_lw = lineups.loc[lineups['game_date'] > date]
lineups = pd.merge(lineups, games, on=['game_pk'])
lineups = pd.merge(lineups, dfHit, left_on=['batter'], right_on=['player_id'])

#to get previous starting pitchers
dfStarters = dfAllData[['game_pk','inning', 'inning_topbot', 'pitcher']] #filter for sp info
dfStarters = dfStarters.loc[dfStarters['inning'] == 1] #grab only pitchers from 1st inning
dfHomeStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Top'] #grab home pitchers from top of 1st
dfHomeStart['sort'] = dfHomeStart['pitcher'].astype(str) + dfHomeStart['game_pk'].astype(str) #create a helper column adding pitcher id to game id to remove duplicates
dfHomeStart = dfHomeStart.drop_duplicates(subset=['sort']) #drop duplicate
dfHomeStart = dfHomeStart[['game_pk', 'pitcher']] #get rid of unneeded columns
dfHomeStart.rename(columns={'pitcher': 'home_starter_id'}, inplace=True) #rename for merging
dfHomeStart = pd.merge(dfHomeStart, dfPit, left_on='home_starter_id', right_on='player_id') #merge pitcher names in
dfHomeStart.rename(columns={'player_name': 'home_sp'}, inplace=True) #rename pitcher columns for home teams
dfHomeStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
# dfHomeStart.to_csv(path.join(DATA_DIR, 'data', 'testing', 'hometeamSP.csv'), index=False, mode='w+')
dfAwayStart = dfStarters.loc[dfStarters['inning_topbot'] == 'Bot'] #all this is the same but for the away starter
dfAwayStart['sort'] = dfAwayStart['pitcher'].astype(str) + dfAwayStart['game_pk'].astype(str)
dfAwayStart = dfAwayStart.drop_duplicates(subset=['sort'])
dfAwayStart = dfAwayStart[['game_pk', 'pitcher']]
dfAwayStart.rename(columns={'pitcher': 'away_starter_id'}, inplace=True)
dfAwayStart = pd.merge(dfAwayStart, dfPit, left_on='away_starter_id', right_on='player_id')
dfAwayStart.rename(columns={'player_name': 'away_sp'}, inplace=True) #rename pitcher columns for home teams
dfAwayStart.drop(['player_id'], axis=1, inplace=True) #clean up the merge
dailyStarters = pd.merge(dfHomeStart, dfAwayStart, on='game_pk')

#merge home and away lineups to one file
dfAwayStart.to_csv(path.join(DATA_DIR, 'data', 'testing', 'awayteamSP.csv'), index=False, mode='w+')
# for i in dfHomeLineup['game_pk'].unique():
#     x = dfHomeLineup[dfHomeLineup['game_pk']==i].head(9)

#narrows the event data to get to relevant columns and simplify the data
dfTestData = dfAllData.loc[(dfAllData['game_date'] < date)]
dfRecentData = dfTestData.loc[(dfTestData['game_date'] >= past_date)]
dfTrimData = dfAllData[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
batting_vs_lhp = dfTrimData.loc[dfTrimData['p_throws'] == 'L']
batting_vs_rhp = dfTrimData.loc[dfTrimData['p_throws'] == 'R']
pitching_vs_lhh = dfTrimData.loc[dfTrimData['stand'] == 'L']
pitching_vs_rhh = dfTrimData.loc[dfTrimData['stand'] == 'R']

#grab homer info
hit_homer = dfAllData.loc[dfAllData['events'] == 'home_run', ['game_date', 'batter', 'pitcher', 'p_throws', 'events', 'launch_angle', 'launch_speed', 'hit_distance_sc', 'bb_type', 'game_pk']]
hit_homer.to_csv(path.join(DATA_DIR, 'data', 'testing', 'homers.csv'), index=False, mode='w+')

#add a column for pa's
dfTrimData['pa'] = (dfTrimData['events'] == 'double' ) | (dfTrimData['events'] == 'double_play' ) | (dfTrimData['events'] == 'field_error' ) |(dfTrimData['events'] == 'field_out' ) |(dfTrimData['events'] == 'fielders_choice' ) |(dfTrimData['events'] == 'fielders_choice_out' ) |(dfTrimData['events'] == 'force_out' ) |(dfTrimData['events'] == 'grounded_into_double_play' ) |(dfTrimData['events'] == 'home_run' ) |(dfTrimData['events'] == 'other_out' ) |(dfTrimData['events'] == 'single' ) |(dfTrimData['events'] == 'strikeout' ) |(dfTrimData['events'] == 'strikeout_double_play' ) |(dfTrimData['events'] == 'triple' ) | (dfTrimData['events'] == 'triple_play' ) | (dfTrimData['events'] == 'catcher_interf' )| (dfTrimData['events'] == 'sac_bunt' )| (dfTrimData['events'] == 'sac_fly' )| (dfTrimData['events'] == 'sac_fly_double_play' )| (dfTrimData['events'] == 'walk' )| (dfTrimData['events'] == 'hit_by_pitch' )
#add a column for atbats
dfTrimData['at_bat'] = (dfTrimData['events'] == 'double' ) | (dfTrimData['events'] == 'double_play' ) | (dfTrimData['events'] == 'field_error' ) |(dfTrimData['events'] == 'field_out' ) |(dfTrimData['events'] == 'fielders_choice' ) |(dfTrimData['events'] == 'fielders_choice_out' ) |(dfTrimData['events'] == 'force_out' ) |(dfTrimData['events'] == 'grounded_into_double_play' ) |(dfTrimData['events'] == 'home_run' ) |(dfTrimData['events'] == 'other_out' ) |(dfTrimData['events'] == 'single' ) |(dfTrimData['events'] == 'strikeout' ) |(dfTrimData['events'] == 'strikeout_double_play' ) |(dfTrimData['events'] == 'triple' ) |(dfTrimData['events'] == 'triple_play' )
#add a column for hits
dfTrimData['hit'] = (dfTrimData['events'] == 'single') | (dfTrimData['events'] == 'double') | (dfTrimData['events'] == 'triple') | (dfTrimData['events'] == 'home_run')
dfTrimData['1B'] = dfTrimData['events'] == 'single'
dfTrimData['2B'] = dfTrimData['events'] == 'double'
dfTrimData['3B'] = dfTrimData['events'] == 'triple'
dfTrimData['HR'] = dfTrimData['events'] == 'home_run'

sum_columns = ['pa', 'at_bat', 'HR']
game_result = dfTrimData.groupby(['game_pk', 'batter']).sum()[sum_columns]
lineups = pd.merge(lineups, game_result, on=['game_pk', 'batter'])
lineups = lineups.sort_values(by=['batter', 'game_date'])

#getSummedStats
dfTrimData.groupby('game_pk').agg( {'pa': 'sum', 'at_bat': 'sum', '1B': 'sum', '2B': 'sum', '3B': 'sum', 'HR': 'sum'}).head()

#***ASSEMBLING BATTER DATA***
#this is for overall batted ball data summarized by batter
dfHit['PA'] = dfHit['player_id'].map(dfTrimData['batter'].value_counts())
is_ball_in_play = dfTrimData.loc[dfTrimData['type'] == 'X']
is_fly_ball = dfTrimData.loc[dfTrimData['bb_type'] == 'fly_ball']
is_home_run = dfTrimData.loc[dfTrimData['events'] == 'home_run']
is_hardhit_FB = dfTrimData.loc[(dfTrimData['bb_type'] == 'fly_ball') & (dfTrimData['launch_speed'] >= 94.5)]
is_hardhit_HR = dfTrimData.loc[(dfTrimData['bb_type'] == 'fly_ball') & (dfTrimData['launch_speed'] >= 94.5) & (dfTrimData['events'] == 'home_run')]
df80thPctEV = is_ball_in_play.groupby('batter')['launch_speed'].quantile(0.80)
dfHit['BIP'] = dfHit['player_id'].map(is_ball_in_play['batter'].value_counts())
dfHit = dfHit.merge((is_ball_in_play.groupby(['batter']).mean()), left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_angle': 'LA-OVR', 'launch_speed': 'EV-Ovr'}, inplace=True)
dfHit['FB'] = dfHit['player_id'].map(is_fly_ball['batter'].value_counts())
dfHit['HR'] = dfHit['player_id'].map(is_home_run['batter'].value_counts())
dfHit['HR/BIP'] = dfHit['HR'] / dfHit['BIP']
dfHit['HH FB'] = dfHit['player_id'].map(is_hardhit_FB['batter'].value_counts())
dfHit['HH HR'] = dfHit['player_id'].map(is_hardhit_HR['batter'].value_counts())
dfHit['PA/HR'] = dfHit['PA'] / dfHit['HR']
dfHit['FB%'] = dfHit['FB'] / dfHit['BIP']
dfHit['HHFB%'] = dfHit['HH FB'] / dfHit['BIP']
dfHit = dfHit.merge(df80thPctEV, left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_speed': '80thPctEV-OVR'}, inplace=True)
dfHit.drop(['pitcher','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs left-handed pitchers
dfHit['PA-vLHP'] = dfHit['player_id'].map(batting_vs_lhp['batter'].value_counts())
is_ball_in_play_vLHP = batting_vs_lhp.loc[batting_vs_lhp['type'] == 'X']
is_fly_ball_vLHP = batting_vs_lhp.loc[batting_vs_lhp['bb_type'] == 'fly_ball']
is_home_run_vLHP = batting_vs_lhp.loc[batting_vs_lhp['events'] == 'home_run']
is_hardhit_FB_vLHP = batting_vs_lhp.loc[(batting_vs_lhp['bb_type'] == 'fly_ball') & (batting_vs_lhp['launch_speed'] >= 94.5)]
is_hardhit_HR_vLHP = batting_vs_lhp.loc[(batting_vs_lhp['bb_type'] == 'fly_ball') & (batting_vs_lhp['launch_speed'] >= 94.5) & (batting_vs_lhp['events'] == 'home_run')]
df80thPctEV_vLHP = is_ball_in_play_vLHP.groupby('batter')['launch_speed'].quantile(0.80)
dfHit['BIP-vLHP'] = dfHit['player_id'].map(is_ball_in_play_vLHP['batter'].value_counts())
dfHit = dfHit.merge((is_ball_in_play_vLHP.groupby(['batter']).mean()), left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_angle': 'LA-vLHP', 'launch_speed': 'EV-vLHP'}, inplace=True)
dfHit['FB-vLHP'] = dfHit['player_id'].map(is_fly_ball_vLHP['batter'].value_counts())
dfHit['HR-vLHP'] = dfHit['player_id'].map(is_home_run_vLHP['batter'].value_counts())
dfHit['HH FB-vLHP'] = dfHit['player_id'].map(is_hardhit_FB_vLHP['batter'].value_counts())
dfHit['HH HR-vLHP'] = dfHit['player_id'].map(is_hardhit_HR_vLHP['batter'].value_counts())
dfHit['PA/HR-vLHP'] = dfHit['PA-vLHP'] / dfHit['HR-vLHP']
dfHit['FB%-vLHP'] = dfHit['FB-vLHP'] / dfHit['BIP-vLHP']
dfHit['HHFB%-vLHP'] = dfHit['HH FB-vLHP'] / dfHit['BIP-vLHP']
dfHit = dfHit.merge(df80thPctEV_vLHP, left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_speed': '80thPctEV-vLHP'}, inplace=True)
dfHit.drop(['pitcher','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs right-handed pitchers
dfHit['PA-vRHP'] = dfHit['player_id'].map(batting_vs_rhp['batter'].value_counts())
is_ball_in_play_vRHP = batting_vs_rhp.loc[batting_vs_rhp['type'] == 'X']
is_fly_ball_vRHP = batting_vs_rhp.loc[batting_vs_rhp['bb_type'] == 'fly_ball']
is_home_run_vRHP = batting_vs_rhp.loc[batting_vs_rhp['events'] == 'home_run']
is_hardhit_FB_vRHP = batting_vs_rhp.loc[(batting_vs_rhp['bb_type'] == 'fly_ball') & (batting_vs_rhp['launch_speed'] >= 94.5)]
is_hardhit_HR_vRHP = batting_vs_rhp.loc[(batting_vs_rhp['bb_type'] == 'fly_ball') & (batting_vs_rhp['launch_speed'] >= 94.5) & (batting_vs_rhp['events'] == 'home_run')]
df80thPctEV_vRHP = is_ball_in_play_vRHP.groupby('batter')['launch_speed'].quantile(0.80)
dfHit['BIP-vRHP'] = dfHit['player_id'].map(is_ball_in_play_vRHP['batter'].value_counts())
dfHit = dfHit.merge((is_ball_in_play_vRHP.groupby(['batter']).mean()), left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_angle': 'LA-vRHP', 'launch_speed': 'EV-vRHP'}, inplace=True)
dfHit['FB-vRHP'] = dfHit['player_id'].map(is_fly_ball_vRHP['batter'].value_counts())
dfHit['HR-vRHP'] = dfHit['player_id'].map(is_home_run_vRHP['batter'].value_counts())
dfHit['HH FB-vRHP'] = dfHit['player_id'].map(is_hardhit_FB_vRHP['batter'].value_counts())
dfHit['HH HR-vRHP'] = dfHit['player_id'].map(is_hardhit_HR_vRHP['batter'].value_counts())
dfHit['PA/HR-vRHP'] = dfHit['PA-vRHP'] / dfHit['HR-vRHP']
dfHit['FB%-vRHP'] = dfHit['FB-vRHP'] / dfHit['BIP-vRHP']
dfHit['HHFB%-vRHP'] = dfHit['HH FB-vRHP'] / dfHit['BIP-vRHP']
dfHit = dfHit.merge(df80thPctEV_vRHP, left_on='player_id', right_on='batter')
dfHit.rename(columns={'launch_speed': '80thPctEV-vRHP'}, inplace=True)
dfHit.drop(['pitcher','game_pk'], axis=1, inplace=True)

dfHit.to_csv(path.join(DATA_DIR, 'data', 'testing', 'hitters2022.csv'), index=False, mode='w+')

#***ASSEMBLING PITCHER DATA***
#adds column for total batters faced (TBF)
dfPit['TBF'] = dfPit['player_id'].map(dfTrimData['pitcher'].value_counts())
is_ball_in_play_pit = dfTrimData.loc[dfTrimData['type'] == 'X']
is_fly_ball_pit = dfTrimData.loc[dfTrimData['bb_type'] == 'fly_ball']
is_home_run_pit = dfTrimData.loc[dfTrimData['events'] == 'home_run']
is_hardhit_FB_pit = dfTrimData.loc[(dfTrimData['bb_type'] == 'fly_ball') & (dfTrimData['launch_speed'] >= 94.5)]
is_hardhit_HR_pit = dfTrimData.loc[(dfTrimData['bb_type'] == 'fly_ball') & (dfTrimData['launch_speed'] >= 94.5) & (dfTrimData['events'] == 'home_run')]
df80thPctEV_pit = is_ball_in_play_pit.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP'] = dfPit['player_id'].map(is_ball_in_play_pit['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_pit.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-OVR', 'launch_speed': 'EV-OVR'}, inplace=True)
dfPit['FB'] = dfPit['player_id'].map(is_fly_ball_pit['pitcher'].value_counts())
dfPit['HR'] = dfPit['player_id'].map(is_home_run_pit['pitcher'].value_counts())
dfPit['HH FB'] = dfPit['player_id'].map(is_hardhit_FB_pit['pitcher'].value_counts())
dfPit['HH HR'] = dfPit['player_id'].map(is_hardhit_HR_pit['pitcher'].value_counts())
dfPit['TBF/HR'] = dfPit['TBF'] / dfPit['HR']
dfPit['FB%'] = dfPit['FB'] / dfPit['BIP']
dfPit['HHFB%'] = dfPit['HH FB'] / dfPit['BIP']
dfPit = dfPit.merge(df80thPctEV_pit, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-OVR'}, inplace=True)
dfPit.drop(['batter','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs left-handed batters
dfPit['TBF-vLHH'] = dfPit['player_id'].map(pitching_vs_lhh['pitcher'].value_counts())
is_ball_in_play_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['type'] == 'X']
is_fly_ball_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['bb_type'] == 'fly_ball']
is_home_run_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['events'] == 'home_run']
is_hardhit_FB_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['bb_type'] == 'fly_ball') & (pitching_vs_lhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['bb_type'] == 'fly_ball') & (pitching_vs_lhh['launch_speed'] >= 94.5) & (pitching_vs_lhh['events'] == 'home_run')]
df80thPctEV_vLHH = is_ball_in_play_vLHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP-vLHH'] = dfPit['player_id'].map(is_ball_in_play_vLHH['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_vLHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-vLHH', 'launch_speed': 'EV-vLHH'}, inplace=True)
dfPit['FB-vLHH'] = dfPit['player_id'].map(is_fly_ball_vLHH['pitcher'].value_counts())
dfPit['HR-vLHH'] = dfPit['player_id'].map(is_home_run_vLHH['pitcher'].value_counts())
dfPit['HH FB-vLHH'] = dfPit['player_id'].map(is_hardhit_FB_vLHH['pitcher'].value_counts())
dfPit['HH HR-vLHH'] = dfPit['player_id'].map(is_hardhit_HR_vLHH['pitcher'].value_counts())
dfPit['TBF/HR-vLHH'] = dfPit['TBF-vLHH'] / dfPit['HR-vLHH']
dfPit['FB%-vLHH'] = dfPit['FB-vLHH'] / dfPit['BIP-vLHH']
dfPit['HHFB%-vLHH'] = dfPit['HH FB-vLHH'] / dfPit['BIP-vLHH']
dfPit = dfPit.merge(df80thPctEV_vLHH, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-vLHH'}, inplace=True)
dfPit.drop(['batter','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs right-handed batters
dfPit['TBF-vRHH'] = dfPit['player_id'].map(pitching_vs_rhh['pitcher'].value_counts())
is_ball_in_play_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['type'] == 'X']
is_fly_ball_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['bb_type'] == 'fly_ball']
is_home_run_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['events'] == 'home_run']
is_hardhit_FB_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['bb_type'] == 'fly_ball') & (pitching_vs_rhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['bb_type'] == 'fly_ball') & (pitching_vs_rhh['launch_speed'] >= 94.5) & (pitching_vs_rhh['events'] == 'home_run')]
df80thPctEV_vRHH = is_ball_in_play_vRHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP-vRHH'] = dfPit['player_id'].map(is_ball_in_play_vRHH['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_vRHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-vRHH', 'launch_speed': 'EV-vRHH'}, inplace=True)
dfPit['FB-vRHH'] = dfPit['player_id'].map(is_fly_ball_vRHH['pitcher'].value_counts())
dfPit['HR-vRHH'] = dfPit['player_id'].map(is_home_run_vRHH['pitcher'].value_counts())
dfPit['HH FB-vRHH'] = dfPit['player_id'].map(is_hardhit_FB_vRHH['pitcher'].value_counts())
dfPit['HH HR-vRHH'] = dfPit['player_id'].map(is_hardhit_HR_vRHH['pitcher'].value_counts())
dfPit['PA/HR-vRHH'] = dfPit['TBF-vRHH'] / dfPit['HR-vRHH']
dfPit['FB%-vRHH'] = dfPit['FB-vRHH'] / dfPit['BIP-vRHH']
dfPit['HHFB%-vRHH'] = dfPit['HH FB-vRHH'] / dfPit['BIP-vRHH']
dfPit = dfPit.merge(df80thPctEV_vRHH, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-vRHH'}, inplace=True)
dfPit.drop(['batter','game_pk'], axis=1, inplace=True)

dfPit.to_csv(path.join(DATA_DIR, 'data', 'testing', 'pitcherstats2022.csv'), index=False, mode='w+')

#Bullpen Filtering



# dfQualifiedPit[['TBF/HR', 'EV-OVR', 'LA-OVR', 'FB%', 'HHFB%', '80thPctEV-OVR']].corr()
# dfQualifiedHit[['PA/HR', 'EV-Ovr', 'LA-OVR', 'FB%', 'HHFB%', '80thPctEV-OVR']].corr()