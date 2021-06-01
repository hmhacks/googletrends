"""
This module cleans and merges scraped Google Trends data.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/11/2021
"""

import os, sys
import pandas as pd

path = "../Data/SearchTerms/"
dirs = os.listdir(path)

def mergeAllSearch():
    """
    Merges all Google search query data from local directory.

    Procedure that produces csv with all search terms, merged on state/date.
    """
    iter = 0
    accum = pd.DataFrame()
    for file in dirs:
        print(file)
        input = "../Data/SearchTerms/" + file
        data = pd.read_csv(input)

        if 'isPartial' in data:
            data = data.drop(['isPartial'], axis =1)

        if iter == 0:
            accum = data
        else:
            accum = pd.merge(accum, data, on = ['State', 'date'], how = 'outer')

        iter += 1

    print(accum.head())
    filename = '../Data/allSearchTerms.csv'
    accum.to_csv(filename, index=True, encoding='utf_8_sig')
