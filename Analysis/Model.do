cap ssc install lassopack
cap ssc install pdslasso

import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/workingData.csv", clear
drop _me stname


global terms = "spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay google_unemployment slutload calvinklein"


elasticnet linear unemployment_rate $terms $iterms if state =="California"
coefpath
