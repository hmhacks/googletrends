"""
This script creates a state-industry level unemployment dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
import bls
import pandas as pd
import csv
import time
# #
# inflation_and_prices1 = bls.get_series('SMU19197802023800001', 2004, 2013)
# # 'SMU  19  19780 20238000 01'
# # SMU40000000000000001
# # SMU00000000000000001
# #
# df = pd.DataFrame(inflation_and_prices1)
# #
# print(df)
# #
# df.to_csv('../Data/ExtractedUnemployment.csv', index=True)
#

def getStateList():
    """
    Uses BLS State Code List to return a list of ints with each state code.
    Link: https://download.bls.gov/pub/time.series/sm/sm.state

    Returns a dictionary with states as keys and codes as values.
    """
    with open('../Data/BLS/StateCodes.csv', newline='') as f:
        reader = csv.reader(f)

        accum = {}
        for row in reader:
            row = str(row)

            state = row[10:-2]
            code = row[2:4]
            accum[state] = code

    del accum['ate_code      state_name']

    return accum


def getIndustryList():
    """
    Uses BLS Industry Code List to return a list of ints with each industry code.
    Link: https://download.bls.gov/pub/time.series/sm/sm.industry

    Returns a dictionary with states as keys and codes as values.
    """
    with open('../Data/BLS/IndustryCodes.csv', newline='') as f:
        reader = csv.reader(f)

        accum = {}
        for row in reader:
            row = str(row)

            state = row[18:-2]
            code = row[2:9]
            accum[state] = code

    del accum['ode   industry_name']

    return accum

def unemployment():
    """
    State and Area Employment, Hours, and Earnings.
    Returns a csv with state-industry-level unemployment rates between 2004 and 2020.
    """
    state_list = list(getStateList().values())
    # state_list = [state_list[40]]
    industry_list = list(getIndustryList().values())
    industry_list = [industry_list[0]]

    accum = pd.DataFrame()
    iter = 0

    for state in state_list:
        for industry in industry_list:
            print(state)
            series = "SMU" + state + "000000000000001"
            print(series)

            # Series Query
            unemployment1 = bls.get_series(series, 2011, 2020)
            df = pd.DataFrame(unemployment1)
            accum = accum.append(df)
            time.sleep(1)

        accum = pd.DataFrame()
        accum.to_csv('../Data/BLS/' + series + '.csv', index=True)




if __name__ == "__main__":
    unemployment()
