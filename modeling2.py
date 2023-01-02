# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:52:53 2022

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
    path.join(DATA_DIR,'data','testing', 'fullseason_qualHit_glmhead.csv').replace("\\","/"))
homeruns = pd.read_csv(
    path.join(DATA_DIR,'data','testing', 'dailyfile.csv').replace("\\","/"))


formula = 't1 ~ t2+t4+t10+t11+t27+t28 '
model2 = smf.glm(formula = formula, data=df, family=sm.families.Poisson())
result = model2.fit()
print(result.summary())

predictions = result.predict()
print(predictions[0:10])

def prob_fbhomer(pfx, la, hhfb, evtoppct, pitlabh, pitkbh):
    b0, b1, b2, b3, b4, b5, b6 = result.params
    return (b0 + b1*pfx + b2*la + b3*hhfb + b4*evtoppct + b5*pitlabh + b6*pitkbh)



homeruns['HR_hat'] = result.predict(homeruns)

homeruns.to_csv(path.join(DATA_DIR, 'data', 'testing', 'dailyfile.csv'), index=False, mode='w+')
