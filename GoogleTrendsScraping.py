"""
This script creates a state level Google search query dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
from pytrends.request import TrendReq
import time

# Only need to run this once, the rest of requests will use the same session.
# pytrends = TrendReq()
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
    requests = len(termList)*timeframe

    accum = pd.DataFrame()
    iter = 0
    for x in range(len(termList)):
        for y in range(len(stateList)):

            stateQuery = 'US-' + stateList[y]

            if (iter + 1)* timeframe < googleLimit:
                try:
                    df = pytrends.get_historical_interest(termList[x], year_start=yearStart, year_end=yearEnd, geo=stateQuery, sleep=0)
                except:
                    pass

                accum = accum.append(df)
                iter += 1

            else:
                time.sleep(90000)
                iter = 0

    accum.to_csv('./Data/GoogleTrends.csv', index=True)
