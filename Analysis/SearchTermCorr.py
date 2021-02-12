"""
Visualizes Google Trend correlation matrix to a heatmap.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/11/2021
"""

import pandas as pd
from string import ascii_letters
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

input = '../Data/allSearchTerms.csv'
data = pd.read_csv(input)
data = data.drop(['Unnamed: 0'], axis =1)
corrMatrix = data.corr()

# National Level
mask = np.triu(np.ones_like(corrMatrix, dtype=bool))
f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(250, 15, as_cmap=True)
sns.heatmap(corrMatrix, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.title("National Google Trends Corollaries by Keyword")
plt.show()

# For each state
states = data.State.unique()

for state in states:
    vis = data.loc[data['State'] == state]
    corrMatrix = vis.corr()

    mask = np.triu(np.ones_like(corrMatrix, dtype=bool))
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(250, 15, as_cmap=True)
    sns.heatmap(corrMatrix, annot=True, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.title( state + " Google Trends Corollaries by Keyword")
    plt.show()
