"""
Henry Manley - hjm67@cornell.edu -  Last Modified 6/7/2021
"""
import pandas as pd
from keywordExtraction import *

# List of states to make queries for
stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
             "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
             "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
             "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
             "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

#How many keywords by source should be queried?
numKeywords = 50

# Parse texts and make all keywords globally available.

################################################################################
# Get Federal Reserve Minutes
################################################################################

FOMCdates = ['20210127', '20210317', '20210428']
fedTexts = ['https://www.federalreserve.gov/monetarypolicy/files/fomcminutes' + x + '.pdf' for x in FOMCdates]

try:
    os.remove("../Data/FOMC2021.txt")
except:
    print("No minutes .txt file found.")

i = 0
for text in fedTexts:
    outfile = '../Data/FOMC' + FOMCdates[i] + '.pdf'
    getTexts(text, outfile)
    parsePDF(outfile, "../Data/FOMC2021.txt")
    i += 1

fed = LDA('../Data/fed2021.txt', 3, numKeywords)


################################################################################
# Shakespeare
################################################################################

getTexts('https://github.com/brunoklein99/deep-learning-notes/blob/master/shakespeare.txt', '../Data/FOMC2021.txt')
shakespeare = LDA('../Data/shakespeare.txt', 5, numKeywords)


################################################################################
# Get Recent BLS Research Papers
################################################################################

BLSindex = [210010, 210020, 210030, 210040, 210050, 210060]
BLSTexts = ['https://www.bls.gov/osmr/research-papers/2021/pdf/ec' + str(x) + '.pdf' for x in BLSindex]

try:
    os.remove("../Data/BLS2021.txt")
except:
    print("No BLS .txt file found.")

i = 0
for text in BLSTexts:
    outfile = '../Data/BLS' + str(BLSindex[i]) + '.pdf'
    getTexts(text, outfile)
    parsePDF(outfile, "../Data/BLS2021.txt")
    i += 1

bls = LDA('../Data/BLS2021.txt', 4, numKeywords)


################################################################################
# Work Literature-based Words
################################################################################

work = ['flights', 'bus', 'pornhub', 'solitaire',  'free apps',
        'guitar scales', 'companies that are hiring', 'jobs near me', 'job openings']

################################################################################
# From the WP https://www.washingtonpost.com/news/wonk/wp/2014/05/30/the-weird-google-searches-of-the-unemployed-and-what-they-say-about-the-economy/
################################################################################

google = ['free apps', 'guitar scales beginner', 'companies that are hiring']

################################################################################
#From D'Amuri 2017 https://www.sciencedirect.com/science/article/pii/S0169207017300389#br000180
################################################################################

dAmuri2017 = ['jobs', 'facebook', 'youtube', 'job center', 'collect unemployment']



# Convert python string to stata local. Needed for multi word keywords.

def pyStrToStaLoc(L):
    assert type(L) == list
    L = ["`" + x + "'" for x in L]
    return L
