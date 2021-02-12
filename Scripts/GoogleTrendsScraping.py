"""
This script creates a state level Google search query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
from pytrends.request import TrendReq
import time
import pandas as pd
import GoogleTrendsCleaning as GTC

pytrends = TrendReq()

# stateList = ['NY', 'IL']

stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def getGoogleTrends(termList, yearStart, yearEnd):
    """
    Returns desired dataset of Google search queries over time.

    Parameter termList represents the search terms to request.
    Preconditon: termList a list of strings

    Parameter yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    Parameter yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int
    """
    assert type(termList) == list

    for term in termList:
        assert type(term) == str

    #Determine sleep time between term requests
    months = 12
    googleLimit = 50000
    timeframe = months*(yearEnd - yearStart)

    accum = pd.DataFrame()
    iter = 0
    for x in range(len(termList)):
        for y in range(len(stateList)):

            stateQuery = 'US-' + stateList[y]

            if (iter + 1)* timeframe < googleLimit:

                data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
                data['State'] = stateList[y]
                accum = accum.append(data)

                iter += 1

            # else:
            #     time.sleep(90000)
            #     data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
            #     data['State'] = stateList[y]
            #     accum = accum.append(data)
            #     iter = 1

        filename = '../Data/SearchTerms/' + termList[x] + '.csv'
        accum.to_csv(filename, index=True, encoding='utf_8_sig')
        accum = pd.DataFrame()


def makeRequest(term, yearStart, yearEnd, stateQuery):
    """
    Builds payload and makes request to Google Trends API.
    Returns request data.

    Parameter term is the kw_list parameter being requested.
    Preconditon term is a list with len 1 (one word at at time)

    Parameter yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    Parameter yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int

    Parameter stateQuery is the state parameter being requested
    Preconditon: stateQuery is a string of format "US-NY", eg.
    """
    pytrends.build_payload(
         kw_list=term,
         cat=0,
         timeframe=  str(yearStart) + '-01-01 ' + str(yearEnd) + '-01-01',
         geo=stateQuery,
         gprop='')

    data = pytrends.interest_over_time()
    time.sleep(1)

    return data

if __name__ == "__main__":
    # getGoogleTrends(['unemployment', 'ebay', 'mens underwear'], 2015, 2019)
    # getGoogleTrends(['cheap gym', 'online masters', 'brownie recipe', 'how to write a cover letter'], 2015, 2019)
    # getGoogleTrends(['coursera', 'how to bake bread', 'google flights'], 2015, 2019)
    # getGoogleTrends(['spider solitaire', 'candy crush', 'harry potter'], 2015, 2019)
    # getGoogleTrends(['porn', 'resume', 'indeed'], 2015, 2019)
    # getGoogleTrends(['pornhub', 'linkedin'], 2015, 2019)
    # getGoogleTrends(['harvard', 'highest paying jobs'], 2015, 2019)

    GTC.mergeAllSearch()
