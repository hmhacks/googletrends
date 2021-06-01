"""
Henry Manley - hjm67@cornell.edu -  Last Modified 5/31/2021
"""

import gtab
from globals import *

def makeNormalizedRequest(keywords, yearStart, yearEnd):
    """
    Master request function. This procedure returns a data set of normalized search
    intensities requested from the Google Trends API. To obtain and evaluate precise
    values, class GTAB is leveraged (Robert West 2021). The returned data is a state-
    month panel.

    @param keywords is a list of keywords to query.
    @param yearStart is the lower year bound to query.
    @param yearEnd is the upper year bound to query.
    """
    timeframe = str(yearStart) + '-01-01 ' + str(yearEnd) + '-01-01'

    # Set Anchor. Initialize GTAB.
    i = 1
    for state in stateList:
        geo = 'US-' + state
        init = gtab.GTAB()
        init.set_options(pytrends_config={"geo": geo, "timeframe": timeframe})

        # Request
        j = 1
        for word in keywords:
            qData = init.new_query(word)
            qData['date'] = qData.index
            qData.reset_index(drop=True, inplace=True)
            qData = qData[["max_ratio", "date"]]
            qData.rename(columns={'max_ratio': word}, inplace=True)

            if j != 1:
                mData = mData.merge(qData, left_on=['date'], right_on = ['date'])
            else:
                mData = qData
            j += 1

        mData['state'] = state

        # Merge State Data
        if i!= 1:
            gData = gData.append(mData, ignore_index=True)
        else:
            gData = mData
        i += 1

    gData.to_csv('../Data/SearchTerms/MASTERDATA.csv', index=True)

makeNormalizedRequest(fed, 2004, 2020)
