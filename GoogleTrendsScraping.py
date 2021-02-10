"""
This script creates a state level Google search query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
from pytrends.request import TrendReq
import time
import pandas as pd

pytrends = TrendReq()


# pytrend = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1)
# keywords = ['fires near me', 'smoke', 'air quality']
#
# pytrends.build_payload(
#      kw_list=keywords,
#      cat=0,
#      timeframe='2019-09-01 2020-04-30',
#      geo='AU-NSW',
#      gprop='')
#
# data = pytrends.interest_over_time()
# data= data.drop(labels=['isPartial'],axis='columns')
# data.to_csv('./Data/Syd_Google_Smoke.csv', encoding='utf_8_sig')
# Only need to run this once, the rest of requests will use the same session.
#
#
# # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
# # pytrend.build_payload(kw_list=['unemployment', 'robinhood'])
#
# kw_list=['unemployment', 'robinhood']
#
# # Interest Over Time
# # interest_over_time_df = pytrend.interest_over_time()
#
# df = pytrends.get_historical_interest(kw_list, year_start=2019, month_start=1, day_start=1, hour_start=0, year_end=2020, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
#
# # print(interest_over_time_df.head())
# print(df.head())
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

            else:
                time.sleep(90000)
                data = makeRequest([termList[x]], yearStart, yearEnd, stateQuery)
                data['State'] = stateList[y]
                accum = accum.append(data)
                iter = 1

        filename = './Data/' + termList[x] + '.csv'
        accum.to_csv(filename, index=True, encoding='utf_8_sig')


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
    data= data.drop(labels=['isPartial'],axis='columns')

    return data

if __name__ == "__main__":
    getGoogleTrends(['cornell'], 2015, 2019)
