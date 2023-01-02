# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 08:10:01 2022

@author: graig

#date filter to get stats up to a date (run 2021analysis_test.py first)
"""
from datetime import datetime
date = datetime(2022, 6, 5)

dfTestData = dfAllData.loc[(dfAllData['game_date'] < date)]
dfTrimData = dfTestData[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
batting_vs_lhp = dfTrimData.loc[dfTrimData['p_throws'] == 'L']
batting_vs_rhp = dfTrimData.loc[dfTrimData['p_throws'] == 'R']
pitching_vs_lhh = dfTrimData.loc[dfTrimData['stand'] == 'L']
pitching_vs_rhh = dfTrimData.loc[dfTrimData['stand'] == 'R']

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