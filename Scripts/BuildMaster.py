"""
This script builds the master dataset, merging Google Trends data
and BLS data on year & state.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/11/2021
"""

import os, sys
import pandas as pd



def buildMaster():
    """
    Merges Google and BLS Data.

    Returns csv.
    """
    google = "../Data/allSearchTerms.csv"
    BLS = "../Data/allBLSSeries.csv"

    google = pd.read_csv(google)
    BLS = pd.read_csv(BLS)

    df= pd.merge(google, BLS, on = ['State', 'date'], how = 'outer')

    print(df.head())
    filename = '../Data/allData.csv'
    df.to_csv(filename, index=True, encoding='utf_8_sig')


if __name__ == "__main__":
    buildMaster()
