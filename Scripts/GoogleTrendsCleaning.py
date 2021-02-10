import os, sys
import pandas as pd

path = "../Data/SearchTerms/"
dirs = os.listdir(path)

def appendAllSearch():
    """
    Merges all Google search query data from local directory.

    Procedure that produces csv with all search terms
    """
    iter = 0
    accum = pd.DataFrame()
    for file in dirs:
        print(file)
        input = "../Data/SearchTerms/" + file
        data = pd.read_csv(input)
        if iter == 0:
            accum.append(data)
        else:
            data.append(data)

    print(data.head())
    filename = '../Data/allSearchTerms.csv'
    data.to_csv(filename, index=True, encoding='utf_8_sig')
    # return data


appendAllSearch()
