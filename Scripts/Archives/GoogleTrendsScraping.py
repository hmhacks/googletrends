"""
This script creates a state level Google search query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
from pytrends.request import TrendReq
import time
import pandas as pd
import GoogleTrendsCleaning as GTC
import requests

pytrends = TrendReq(retries=10, backoff_factor=0.5)


stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def getGoogleTrends(termList, yearStart, yearEnd, keywordList=False):
    """
    Returns desired dataset of Google search queries over time.

    @param termList represents the search terms to request.
    Preconditon: termList a list of strings

    @param yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    @param yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int
    """
    assert type(termList) == list

    for term in termList:
        assert type(term) == str or type(term) == list

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
                if keywordList:
                    data = makeRequest(termList[0], yearStart, yearEnd, stateQuery)
                    time.sleep(1)
                else:
                    data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
                    time.sleep(1)

                data['State'] = stateList[y]
                accum = accum.append(data)
                iter += 1

        filename = '../Data/SearchTerms/' + str(termList[x]) + '.csv'
        accum.to_csv(filename, index=True, encoding='utf_8_sig')
        accum = pd.DataFrame()


def makeRequest(term, yearStart, yearEnd, stateQuery):
    """
    Builds payload and makes request to Google Trends API.
    Returns request data.

    @param term is the kw_list parameter being requested.
    Preconditon term is a list with len 1 (one word at at time)

    @param yearStart is the lower bound of the time series.
    Preconditon: yearStart is an int

    @param yearEnd is the upper bound of the time series.
    Preconditon: yearEnd is an int

    @param stateQuery is the state parameter being requested
    Preconditon: stateQuery is a string of format "US-NY", eg.
    """
    try:
        pytrends.build_payload(
             kw_list=term,
             cat=0,
             timeframe=  str(yearStart) + '-01-01 ' + str(yearEnd) + '-01-01',
             geo=stateQuery,
             gprop='')

    except requests.exceptions.Timeout:
        print("Timeout occured")


    data = pytrends.interest_over_time()
    return data

    # https://github.com/mdroste/stata-pylearn

if __name__ == "__main__":
    # getGoogleTrends(['unemployment'], 2011, 2019)
    # getGoogleTrends(['spider solitaire'], 2011, 2019)
    # getGoogleTrends(['pornhub'], 2011, 2019)
    # getGoogleTrends(['google flights'], 2011, 2019)
    # getGoogleTrends(['jobs near me'], 2011, 2019)
    # getGoogleTrends(['omegle'], 2011, 2019)
    # getGoogleTrends(['candy crush'], 2011, 2019)
    # getGoogleTrends(['linkedin'], 2011, 2019)
    # getGoogleTrends(['xbox'], 2011, 2019)
    # getGoogleTrends(['harvard'], 2011, 2019)
    # getGoogleTrends(['brownie recipe'], 2011, 2019)
    # getGoogleTrends(['blood drive'], 2011, 2019)
    # getGoogleTrends(['resume template'], 2011, 2019)
    # getGoogleTrends(['slutload'], 2011, 2019)
    # getGoogleTrends(['ebay'], 2011, 2019)
    # getGoogleTrends(['y combinator'], 2011, 2019)
    # getGoogleTrends(['calvin klein'], 2011, 2019)

    # getGoogleTrends(['vodka'], 2011, 2019)
    # getGoogleTrends(['jobs'], 2011, 2019)
    # getGoogleTrends(['haircut'], 2011, 2019)
    # getGoogleTrends(['lottery'], 2011, 2019)
    # getGoogleTrends(['google flights'], 2008, 2019)
    # getGoogleTrends(['pornhub'], 2008, 2019)
    # getGoogleTrends(['unemployment'], 2008, 2020)
    # getGoogleTrends(['google flights'], 2008, 2020)
    # getGoogleTrends(['pornhub'], 2008, 2020)
    # getGoogleTrends(['haircut'], 2008, 2020)
    # getGoogleTrends(['mens underwear'], 2008, 2020)
    GTC.mergeAllSearch()
