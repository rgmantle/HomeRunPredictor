# -*- coding: utf-8 -*-
"""
Created on Tue May 31 21:01:15 2022

@author: graig
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from os import path


DATA_DIR = '/Users/graig/Documents/BaseballBets'
df = pd.read_csv(path.join(DATA_DIR, 'data', 'homers.csv'))

g = sns.displot(x='Bat-EV', y='Distance', col='Pitch', col_wrap=3, data=df)

df['Ballpark'].value_counts()

df['Inning'].value_counts()

df['Team'].value_counts()

df['Pitch'].value_counts()

df[['Team', 'Ballpark', 'Date']].value_counts().head(395)

df[['Inning', 'Pitcher']].value_counts()

df[['Bat-FB%', 'Bat-HR/FB', 'Bat-SLG', 'Bat-ISO']].quantile(.1)

multiHRdf = df[['Team', 'Ballpark', 'Date', 'Batter']]

multiHRdf.to_csv(path.join(DATA_DIR, 'data', 'multiHRgame.csv'), index=False, mode='w+')
