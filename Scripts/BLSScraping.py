"""
This script creates a state level unemployment dataset.

Henry Manley - hjm67@cornell.edu -  Last Modified 2/8/2021
"""
import bls
import pandas as pd
import csv
import time
import BLSCleaning as BLSC
# Demo
# inflation_and_prices1 = bls.get_series('SMU00000000000000001', 2004, 2013)
# df = pd.DataFrame(inflation_and_prices1)
# print(df.head())
# df.to_csv('../Data/ExtractedUnemployment.csv', index=True)

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

def mapState(id):
    """
    Maps state ID number to two-letter state abbreviation.

    Parameter id is the state ID.
    Precondition: id is a str
    """
    id = str(id)

    with open('../Data/BLS/StateCodes.csv', newline='') as f:
        reader = csv.reader(f)
        accum = []
        for row in reader:
            row = str(row)
            state = row[10:-2]
            code = row[2:4]
            accum.append([state, code])
    BLS_state_code = accum

    with open('../Data/BLS/StateAbbrev.csv', newline='') as f:
        reader = csv.reader(f)
        accum = []
        for row in reader:
            row = str(row)
            dash = row.index('-')
            state = row[2:dash-1]
            abbrev= row[dash + 2:-2]
            accum.append([state, abbrev])
    state_abbrev = accum

    for pair in BLS_state_code:
        if id == pair[1]:
            STATE = pair[0]
            for coup in state_abbrev:
                if STATE == coup[0]:
                    return coup[1]


def unemployment():
    """
    State and Area Employment, Hours, and Earnings.
    Returns a csv with state-industry-level unemployment rates between 2004 and 2020.
    """
    # Request Parameters
    state_list = list(getStateList().values())
    state_list = state_list[1:-3]

    prefix = 'LN'
    seasonal = 'S'
    area = '00000'
    industry = '00000000'
    data_type = '01'
    LNS12300000

    master = pd.DataFrame()
    iter = 0

    for state in state_list:
        accum = pd.DataFrame()
        print(state)
        series = prefix + seasonal + state + area + industry + data_type
        print(series)

        # Series Query
        unemployment1 = bls.get_series(series, 2015, 2020)
        df = pd.DataFrame(unemployment1)
        accum = accum.append(df)
        accum['State'] = mapState(state)

        master = master.append(accum)
        accum = pd.DataFrame()

        iter +=1

        if iter == 20:
            time.sleep(50000)
            iter == 0


    master.to_csv('../Data/BLS/' + series + '.csv', index=True)


if __name__ == "__main__":
    unemployment()
    BLSC.mergeAllBLS()
