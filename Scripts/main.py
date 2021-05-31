"""
Calls all query modules to produce time series data for normalized keywords.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/25/2021
"""
from keywordExtraction import *
from GoogleTrendsScraping import *

# Parse texts and extract keywords
parsePDF('../Data/fomc2021.pdf', "../Data/fed2021.txt")
fed = getKeywords("../Data/fed2021.txt", 6)
shakespeare =getKeywords('../Data/shakespeare.txt', 5)


def makeKey(kList):
    """
    From a keyword list, request and normalize time series data from Trends API.

    This procedure yields local csvs which all include data on the groupings key.
    The key is one trivial index that will be used to compare one request group with
    another group, overcoming group size limits. This key is simply the most frequent
    keyword, or list index 0 of kList.

    @param kList is a list of strings.
    """

    #Get each keyword data individually. This is less important
    # for keyword in kList:
    #     print(keyword)
    #     getGoogleTrends([keyword], 2011, 2019)
    #     GTC.mergeAllSearch()
    #     time.sleep(10)

    # Now concurrently and pegged to key
    if len(kList) > 5:
        key = kList[0]
        kList = kList[1:]
        L = len(kList)

        i = 0
        while L//4 > 0:

            requestL = [key] + kList[i:i + 4]
            # getGoogleTrends([requestL], 2011, 2019, keywordList=True)ß
            L -= 4
            i += 4

        requestL = [key] + kList[i:len(kList)]
        getGoogleTrends([requestL], 2011, 2019, keywordList=True)

    else:
        getGoogleTrends([kList], 2011, 2019, keywordList=True)


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
    return data


# makeKey(fed)
d = normalize(fed[0])
print(d)
