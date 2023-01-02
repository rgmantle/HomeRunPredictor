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
    path.join(DATA_DIR,'data','testing', 'dailyfile2.csv').replace("\\","/"))


formula = 't1 ~ t2+t4+ t7+t11+t26'
model2 = smf.glm(formula = formula, data=df, family=sm.families.Poisson())
result = model2.fit()
print(result.summary())

predictions = result.predict()
print(predictions[0:10])

def prob_fbhomer(pfx, la, hrbip, evtoppct, pitevbh):
    b0, b1, b2, b3, b4, b5 = result.params
    return (b0 + b1*pfx + b2*la + b3*hrbip + b4*evtoppct + b5*pitevbh)



homeruns['HR_hat'] = result.predict(homeruns)

homeruns.to_csv(path.join(DATA_DIR, 'data', 'testing', 'dailyfile2.csv'), index=False, mode='w+')
