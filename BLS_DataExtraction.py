"""
This script creates a state-industry level unemployment dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
import bls
import pandas as pd
import csv
import time

# inflation_and_prices1 = bls.get_series('CUUR0000SA0', 2004, 2013)
# df = pd.DataFrame(inflation_and_prices1)
#
# print(df)

#Unemployment by state and industry
#   Splitting into two df's allows the bypass of BLS API requirements

def getStateList():
    """
    Uses BLS State Code List to return a list of ints with each state code.
    Link: https://download.bls.gov/pub/time.series/sm/sm.state

    Returns a dictionary with states as keys and codes as values.
    """
    with open('./Data/StateCodes.csv', newline='') as f:
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
    with open('./Data/IndustryCodes.csv', newline='') as f:
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
    State and Area Employment, Hours, and Earnings
    Returns a Pandas df with state-industry-level unemployment rates between 2004 and 2020.
    """
    state_list = list(getStateList().values())
    industry_list = list(getIndustryList().values())

    accum = pd.DataFrame()
    iter = 0

    for state in state_list:
        for industry in industry_list:

            if iter < 450:
                try :
                    series = "SMU" + state + "00000" + industry +"01"
                    print(series)
                    # Series Query
                    unemployment1 = bls.get_series(series, 2004, 2020)
                    df = pd.DataFrame(unemployment1)
                    accum = accum.append(df)

                except:
                    pass

            else:
                #waits 25 hours
                time.sleep(90000)
                iter = 0

            iter += 1

    return accum





# print(unemployment())
#work on downstream datawork
