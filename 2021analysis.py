# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 19:28:18 2022

@author: graig
"""
import pandas as pd
from os import path

DATA_DIR = '/Users/graig/Documents/BaseballBets'

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

#narrows the event data to get to relevant columns and simplify the data
dfTrimData = dfAllData[['batter', 'pitcher', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'game_pk']]
batting_vs_lhp = dfTrimData.loc[dfTrimData['p_throws'] == 'L']
batting_vs_rhp = dfTrimData.loc[dfTrimData['p_throws'] == 'R']
pitching_vs_lhh = dfTrimData.loc[dfTrimData['stand'] == 'L']
pitching_vs_rhh = dfTrimData.loc[dfTrimData['stand'] == 'R']
dfBullpen = dfAllData[['home_team', 'away_team', 'events', 'description', 'stand', 'p_throws', 'type', 'bb_type', 'launch_speed', 'launch_angle', 'inning', 'inning_topbot', 'game_pk']]

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

#filter out for minimum 150 plate appearances total and add percentile columns
dfQualifiedHit = dfHit.loc[dfHit['PA'] >= 150]
dfQualifiedHit['EV-80thPct'] = dfQualifiedHit['80thPctEV-OVR'].rank(pct = True)
dfQualifiedHit['HHFB-Pct'] = dfQualifiedHit['HHFB%'].rank(pct = True)
dfQualifiedHit['EV-80thPct-vLHP'] = dfQualifiedHit['80thPctEV-vLHP'].rank(pct = True)
dfQualifiedHit['HHFB-Pct-vLHP'] = dfQualifiedHit['HHFB%-vLHP'].rank(pct = True)
dfQualifiedHit['EV-80thPct-vRHP'] = dfQualifiedHit['80thPctEV-vRHP'].rank(pct = True)
dfQualifiedHit['HHFB-Pct-vRHP'] = dfQualifiedHit['HHFB%-vRHP'].rank(pct = True)


#take, in this case, the 70th percentile hitters in hard hit fly ball percentage
# dfTopHitters = dfQualifiedHit.loc[dfQualifiedHit['EV-80thPct'] >= 0.70]
# dfTopHittersvLHP = dfQualifiedHit.loc[dfQualifiedHit['EV-80thPct-vLHP'] >= 0.70]
# dfTopHittersvRHP = dfQualifiedHit.loc[dfQualifiedHit['EV-80thPct-vRHP'] >= 0.70]
dfHit.to_csv(path.join(DATA_DIR, 'data', 'savant', 'hitters2022.csv'), index=False, mode='w+')
# dfTopHitters.to_csv(path.join(DATA_DIR, 'data', 'savant', 'tophitters2022.csv'), index=False, mode='w+')

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
is_strikeout_vLHH = pitching_vs_lhh.loc[pitching_vs_lhh['events'] == 'strikeout']
is_hardhit_FB_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['bb_type'] == 'fly_ball') & (pitching_vs_lhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vLHH = pitching_vs_lhh.loc[(pitching_vs_lhh['bb_type'] == 'fly_ball') & (pitching_vs_lhh['launch_speed'] >= 94.5) & (pitching_vs_lhh['events'] == 'home_run')]
df80thPctEV_vLHH = is_ball_in_play_vLHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP-vLHH'] = dfPit['player_id'].map(is_ball_in_play_vLHH['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_vLHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-vLHH', 'launch_speed': 'EV-vLHH'}, inplace=True)
dfPit['FB-vLHH'] = dfPit['player_id'].map(is_fly_ball_vLHH['pitcher'].value_counts())
dfPit['HR-vLHH'] = dfPit['player_id'].map(is_home_run_vLHH['pitcher'].value_counts())
dfPit['K-vLHH'] = dfPit['player_id'].map(is_strikeout_vLHH['pitcher'].value_counts())
dfPit['HH FB-vLHH'] = dfPit['player_id'].map(is_hardhit_FB_vLHH['pitcher'].value_counts())
dfPit['HH HR-vLHH'] = dfPit['player_id'].map(is_hardhit_HR_vLHH['pitcher'].value_counts())
dfPit['TBF/HR-vLHH'] = dfPit['TBF-vLHH'] / dfPit['HR-vLHH']
dfPit['FB%-vLHH'] = dfPit['FB-vLHH'] / dfPit['BIP-vLHH']
dfPit['HHFB%-vLHH'] = dfPit['HH FB-vLHH'] / dfPit['BIP-vLHH']
dfPit['K%-vsLHH'] = dfPit['K-vLHH'] / dfPit['TBF-vLHH']
dfPit = dfPit.merge(df80thPctEV_vLHH, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-vLHH'}, inplace=True)
dfPit.drop(['batter','game_pk'], axis=1, inplace=True)

#filtered for plate appearances vs right-handed batters
dfPit['TBF-vRHH'] = dfPit['player_id'].map(pitching_vs_rhh['pitcher'].value_counts())
is_ball_in_play_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['type'] == 'X']
is_fly_ball_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['bb_type'] == 'fly_ball']
is_home_run_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['events'] == 'home_run']
is_strikeout_vRHH = pitching_vs_rhh.loc[pitching_vs_rhh['events'] == 'strikeout']
is_hardhit_FB_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['bb_type'] == 'fly_ball') & (pitching_vs_rhh['launch_speed'] >= 94.5)]
is_hardhit_HR_vRHH = pitching_vs_rhh.loc[(pitching_vs_rhh['bb_type'] == 'fly_ball') & (pitching_vs_rhh['launch_speed'] >= 94.5) & (pitching_vs_rhh['events'] == 'home_run')]
df80thPctEV_vRHH = is_ball_in_play_vRHH.groupby('pitcher')['launch_speed'].quantile(0.80)
dfPit['BIP-vRHH'] = dfPit['player_id'].map(is_ball_in_play_vRHH['pitcher'].value_counts())
dfPit = dfPit.merge((is_ball_in_play_vRHH.groupby(['pitcher']).mean()), left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_angle': 'LA-vRHH', 'launch_speed': 'EV-vRHH'}, inplace=True)
dfPit['FB-vRHH'] = dfPit['player_id'].map(is_fly_ball_vRHH['pitcher'].value_counts())
dfPit['HR-vRHH'] = dfPit['player_id'].map(is_home_run_vRHH['pitcher'].value_counts())
dfPit['K-vRHH'] = dfPit['player_id'].map(is_strikeout_vRHH['pitcher'].value_counts())
dfPit['HH FB-vRHH'] = dfPit['player_id'].map(is_hardhit_FB_vRHH['pitcher'].value_counts())
dfPit['HH HR-vRHH'] = dfPit['player_id'].map(is_hardhit_HR_vRHH['pitcher'].value_counts())
dfPit['PA/HR-vRHH'] = dfPit['TBF-vRHH'] / dfPit['HR-vRHH']
dfPit['FB%-vRHH'] = dfPit['FB-vRHH'] / dfPit['BIP-vRHH']
dfPit['HHFB%-vRHH'] = dfPit['HH FB-vRHH'] / dfPit['BIP-vRHH']
dfPit['K%-vsRHH'] = dfPit['K-vRHH'] / dfPit['TBF-vRHH']
dfPit = dfPit.merge(df80thPctEV_vRHH, left_on='player_id', right_on='pitcher')
dfPit.rename(columns={'launch_speed': '80thPctEV-vRHH'}, inplace=True)
dfPit.drop(['batter','game_pk'], axis=1, inplace=True)

dfQualifiedPit = dfPit.loc[dfPit['TBF'] >= 200]
dfQualifiedPit['EV-Pct'] = dfQualifiedPit['EV-OVR'].rank(pct = True)
dfQualifiedPit['HHFB-Pct'] = dfQualifiedPit['HHFB%'].rank(pct = True)

# dfWorstPitchers = dfQualifiedPit.loc[dfQualifiedPit['HHFB-Pct'] >= 0.60]

dfPit.to_csv(path.join(DATA_DIR, 'data', 'savant', 'pitcherstats2022.csv'), index=False, mode='w+')
# dfWorstPitchers.to_csv(path.join(DATA_DIR, 'data', 'savant', 'worstPitchers2022.csv'), index=False, mode='w+')

#Bullpen Filtering
# dfHomeBullpen = dfBullpen.loc[(dfBullpen['inning'] >= 7) & (dfBullpen['inning_topbot'] == 'Top')]
# dfHomeBullpen.drop('away_team', axis=1, inplace=True)
# dfHomeBullpen.rename(columns={'home_team': 'team'}, inplace=True)
# dfAwayBullpen = dfBullpen.loc[(dfBullpen['inning'] >= 7) & (dfBullpen['inning_topbot'] == 'Bot')]
# dfAwayBullpen.drop('home_team', axis=1, inplace=True)
# dfAwayBullpen.rename(columns={'away_team': 'team'}, inplace=True)
# dfHomeBullpen.append(dfAwayBullpen, ignore_index = True)

# dfPen = dfTeam[['ABR', 'Team']]
# dfPen['TBF'] = dfTeam['ABR'].map(dfHomeBullpen['team'].value_counts())
# is_ball_in_play_bp = dfHomeBullpen.loc[dfHomeBullpen['type'] == 'X']
# is_fly_ball_bp = dfHomeBullpen.loc[dfHomeBullpen['bb_type'] == 'fly_ball']
# is_home_run_bp = dfHomeBullpen.loc[dfHomeBullpen['events'] == 'home_run']
# is_hardhit_FB_bp = dfHomeBullpen.loc[(dfHomeBullpen['bb_type'] == 'fly_ball') & (dfHomeBullpen['launch_speed'] >= 94.5)]
# is_hardhit_HR_bp = dfHomeBullpen.loc[(dfHomeBullpen['bb_type'] == 'fly_ball') & (dfHomeBullpen['launch_speed'] >= 94.5) & (dfHomeBullpen['events'] == 'home_run')]
# df80thPctEV_bp = is_ball_in_play_bp.groupby('team')['launch_speed'].quantile(0.80)
# df80thPctLA_bp = is_ball_in_play_bp.groupby('team')['launch_angle'].quantile(0.80)
# dfPen['BIP'] = dfPen['ABR'].map(is_ball_in_play_bp['team'].value_counts())
# dfPen = dfPen.merge((is_ball_in_play_bp.groupby(['team']).mean()), left_on='ABR', right_on='team')
# dfPen.rename(columns={'launch_angle': 'LA-OVR', 'launch_speed': 'EV-OVR'}, inplace=True)
# dfPen['FB'] = dfPen['ABR'].map(is_fly_ball_bp['team'].value_counts())
# dfPen['HR'] = dfPen['ABR'].map(is_home_run_bp['team'].value_counts())
# dfPen['HH FB'] = dfPen['ABR'].map(is_hardhit_FB_bp['team'].value_counts())
# dfPen['HH HR'] = dfPen['ABR'].map(is_hardhit_HR_bp['team'].value_counts())
# dfPen['TBF/HR'] = dfPen['TBF'] / dfPen['HR']
# dfPen['FB%'] = dfPen['FB'] / dfPen['BIP']
# dfPen['HHFB%'] = dfPen['HH FB'] / dfPen['BIP']
# dfPen = dfPen.merge(df80thPctEV_bp, left_on='ABR', right_on='team')
# dfPen.rename(columns={'launch_speed': '80thPctEV-OVR'}, inplace=True)
# dfPen = dfPen.merge(df80thPctLA_bp, left_on='ABR', right_on='team')
# dfPen.rename(columns={'launch_angle': '80thPctLA-OVR'}, inplace=True)
# dfPen.drop(['inning','game_pk'], axis=1, inplace=True)

# dfPen.to_csv(path.join(DATA_DIR, 'data', 'savant', 'bullpen2022.csv'), index=False, mode='w+')



# dfQualifiedPit[['TBF/HR', 'EV-OVR', 'LA-OVR', 'FB%', 'HHFB%', '80thPctEV-OVR']].corr()
# dfQualifiedHit[['PA/HR', 'EV-Ovr', 'LA-OVR', 'FB%', 'HHFB%', '80thPctEV-OVR']].corr()