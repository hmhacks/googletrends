import pandas as pd
from keywordExtraction import *

# List of states to make queries for


stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC"]
# stateList = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
#           "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
#           "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
#           "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
#           "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


# Parse texts and make all keywords globally available. How many keywords by source
# should be queried?
numKeywords = 5
parsePDF('../Data/fomc2021.pdf', "../Data/fed2021.txt")
fed = getKeywords("../Data/fed2021.txt", numKeywords)
shakespeare =getKeywords('../Data/shakespeare.txt', numKeywords)

work = []
literature = []
