"""
This module creates a state level BLS series query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/11/2021
"""

import os, sys
import pandas as pd

path = "../Data/BLS/"
dirs = os.listdir(path)

def mergeAllBLS():
    """
    Merges all BLS data from local directory.

    Procedure that produces csv with all series, merged on state/date.
    """
    iter = 0
    accum = pd.DataFrame()
    for file in dirs:
        if 'SMU' in file:
            input = "../Data/BLS/" + file
            data = pd.read_csv(input)

            if 'isPartial' in data:
                data = data.drop(['isPartial'], axis =1)

            if iter == 0:
                accum = data
            else:
                accum = pd.merge(accum, data, on = ['State', 'date'], how = 'outer')

            iter += 1

    print(accum.head())
    filename = '../Data/allBLSSeries.csv'
    accum.to_csv(filename, index=True, encoding='utf_8_sig')
