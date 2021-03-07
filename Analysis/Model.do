cap ssc install lassopack
cap ssc install pdslasso

import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/workingData.csv", clear
drop _me stname


global terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay google_unemployment slutload calvinklein"


xtset fips
xteregress unemployment_rate i.fips $terms##$terms
