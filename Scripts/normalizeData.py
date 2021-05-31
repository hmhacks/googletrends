"""
This script normalizes Google Trends data, combining information from
relative queries (ones where a list of keywords are on the same time series and
relative to each other) and singleton queries.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
import os
import pandas as pd


def normalize(key=''):
    """
    To overcome the limitations of the Google Trends API, this function returns a panel
    normalized to one index. This allows for more relative, and perhaps more sensative
    forecasting models.

    @param key is the index of type string that all time series will be normalized to.
    """

    i = 1
    for file in sorted(os.listdir('../Data/SearchTerms')):
        if file.endswith('\'].csv') and key in file:
            localData = pd.read_csv('../Data/SearchTerms/' + file)

            if i != 1:
                data = data.merge(localData, left_on=['date', 'State'], right_on = ['date', 'State'])
            else:
                data = localData
            i += 1
    print(data)

normalize()

    #
    # cols = data.columns.values.tolist()
    # cols.remove('date')
    # cols.remove('isPartial')
    # cols.remove('State')
    #
    # states  = data['State'].unique()
    # localData = data[cols]
    #
    # for state in states:
    #     localMax = []
    #     for keyword in cols:
    #         localData = data[[keyword, 'State']]
    #         keyMax = localData[(localData['State'] == state)].max().values
    #         keyMax = keyMax[0]
    #         localMax.append([keyword, keyMax])
    #
    #     maxValue = 0
    #     maxWord = ""
    #     for pair in localMax:
    #         if pair[1] > maxValue:
    #             maxValue = pair[1]
    #             maxWord = pair[0]
    #
    #     for keyword in cols:
    #         print(state)
    #         print(keyword)
    #
    #         if keyword != maxWord:
    #             # data[[keyword]]['State' == state] = data[[keyword]]/maxValue
    #             data.loc[data['State'] == state, [keyword]] = data[[keyword]]/maxValue
    #
    # print(data)
