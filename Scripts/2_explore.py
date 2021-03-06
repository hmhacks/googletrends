"""
Henry Manley - hjm67@cornell.edu -  Last Modified 6/15/2021
"""
import gtab
import traceback
from globals import *
from datetime import date, timedelta
from calendar import monthrange
import time as tF


def get_last_date_of_month(year: int, month: int) -> date:
    """
    Given a year and a month returns an instance of the date class
    containing the last day of the corresponding month.
    Source: https://stackoverflow.com/questions/42950/get-last-day-of-the-month-in-python
    """
    return date(year, month, monthrange(year, month)[1])


def convert_dates_to_timeframe(start: date, stop: date) -> str:
    """
    Given two dates, returns a stringified version of the interval between
    the two dates which is used to retrieve data for a specific time frame
    from Google Trends.
    Source: https://github.com/GeneralMills/pytrends/blob/master/pytrends/dailydata.py
    """
    return f"{start.strftime('%Y-%m-%d')} {stop.strftime('%Y-%m-%d')}"


def timeEstimate(keywords, waitTime):
    """
    Calculate the number of iterations needed to request the data and the time
    (in minutes) it is estimated to make such requests for all 50 states.

    @param keywords is a list of keywords to query.
    @param waitTIme is the sleep time specified in makeNormalizedRequest().
    """
    requestN = len(keywords) * 50
    requestT = requestN/10  + requestN*waitTime
    return [requestN, requestT]


def makeNormalizedRequest(keywords, yearStart, yearEnd, fileName, waitTime = 0):
    """
    Master request function. This procedure returns a data set of normalized search
    intensities requested from the Google Trends API. To obtain and evaluate precise
    values, class GTAB is leveraged (Robert West 2021). The returned data is a state-
    month panel.

    @param keywords is a list of keywords to query.
    @param yearStart is the lower year bound to query.
    @param yearEnd is the upper year bound to query.
    @param fileName is some unique strinf to precede file name when data is returned.
    """
    assert type(keywords) == list
    assert type(fileName) == str

    # Get Time Estimate
    time = timeEstimate(keywords, waitTime)[0]

    # Set request time parameters
    start_date = date(yearStart, 1, 1)
    stop_date = get_last_date_of_month(yearEnd, 12)
    timeframe = convert_dates_to_timeframe(start_date, stop_date)

    # Set Anchor. Initialize GTAB.
    badKeywords = []
    i = 1
    progress = 1
    for state in stateList:
        geo = 'US-' + state
        init = gtab.GTAB()
        init.set_options(pytrends_config={"geo": geo, "timeframe": timeframe})

        # Request. Try proxy until it works.
        j = 1
        for word in keywords:
            # Sleep and Progress Display
            tF.sleep(waitTime)
            progress += 1
            print(fileName + "- "  + str(progress) + " requests out of " + str(time) + " made.")

            # Skip bad keywords
            if i != 1:
                if word in badKeywords:
                    continue

            try:
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

            except Exception as e:
                if i == 1:
                    badKeywords.append(word)

        mData['state'] = state

        # Merge State Data
        if i!= 1:
            gData = gData.append(mData, ignore_index=True)
        else:
            gData = mData
        i += 1

    gData.date.astype('datetime64[ns]')
    gData.to_csv('../Data/SearchTerms/' + fileName + '.csv', index=True)

makeNormalizedRequest(work, 2004, 2020, 'work', 1)
makeNormalizedRequest(fed, 2004, 2020, 'fed', 1)
makeNormalizedRequest(shakespeare, 2004, 2020, 'shakespeare', 1)
makeNormalizedRequest(google, 2004, 2020, 'google', 1)
makeNormalizedRequest(dAmuri2017, 2004, 2020, 'DAmuri2017', 1)
