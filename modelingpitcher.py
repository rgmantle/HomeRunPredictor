# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:28:20 2022

@author: graig
"""

import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
import numpy as np

DATA_DIR = '/Users/graig/Documents/BaseballBets'

df = pd.read_csv(
    path.join(DATA_DIR,'data','testing', 'fullseason_split_only_whead.csv').replace("\\","/"))
homeruns = pd.read_csv(
    path.join(DATA_DIR,'data','testing', 'dailyfile2.csv').replace("\\","/"))


formula = 't1 ~ t2+t14+t15+t17'
model2 = smf.glm(formula = formula, data=df, family=sm.families.Poisson())
result = model2.fit()
print(result.summary())

predictions = result.predict()
print(predictions[0:10])

def prob_fbhomer(pfx, hrbip, fbrt, evph):
    b0, b1, b2, b3, b4 = result.params
    return (b0 + b1*pfx + b2*hrbip + b3*fbrt + b4*evph)



homeruns['HR_hat'] = result.predict(homeruns)

homeruns.to_csv(path.join(DATA_DIR, 'data', 'testing', 'dailyfile.csv'), index=False, mode='w+')