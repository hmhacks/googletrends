"""
Model Horserace. Configure and access Stata from Python.

Henry Manley - hjm67@cornell.edu -  Last Modified 5/31/2021
"""

import stata_setup
stata_setup.config('/Applications/Stata/', 'be')

from pystata import stata
from sfi import Macro
from globals import *
import os

stata.config.init('be')
stata.config.set_graph_show(True, perm=False)
path = os.path.abspath(os.path.join(os.getcwd(),".."))
Macro.setGlobal('data', path + '/Data')
Macro.setGlobal('analysis', path + '/Analysis')

# Build global data
stata.run(
    """
    * State fips
    import delimited "$data/statefips.csv", clear
	rename stusps state
	replace state = subinstr(state, " ","",.)
	tempfile working
	save `working',replace

    * Search Terms
    import delimited "$data/SearchTerms/MASTERDATA", clear
    gen month = substr(date, 6,2)
    gen year = substr(date,1, 4)
	destring month, replace
	destring year, replace

    merge m:1 state using `working'
    drop _me
    rename st fips
    save `working', replace

    * Unemployment
	import excel "../TESTING.xlsx", sheet("ststdsadata") clear
	rename A fips
	rename B state
	rename C year
	rename D month
	rename E civ_pop
	rename F civ_pop_working_age
	rename G percent_working_age
	rename H employed
	rename I percent_employed
	rename J unemployed
	rename K unemployment_rate
	drop in 1/8

    gen date = month + "/" + year
	gen date1 = date(date, "MY")
	gen compare = date1

	sort state year month
    by state: gen lag = date1[_n-1]
	format lag %td
	format date1 %td
	rename date1 lead
	drop date

	ds
	local vlist = r(varlist)
	foreach y of local vlist{
		cap destring `y', replace
	}

	duplicates drop month year fips, force

	save "/$data/unemploymentMaster", replace
	cap drop date

	merge 1:1 month year fips using `working', force
	keep if _me ==3
    drop _me

    list in 1/3

    """)

# Stata Config. & Training - Testing Split & Test MSE Function
stata.run(
    """
    cap prog drop configStata
    prog def configStata
        cd "$analysis"
        set graphics on
        xtset fips
    end


    cap prog drop splitData
    prog def splitData
        syntax, seed(integer)
        set seed `seed'
        cap drop train yhat
        gen train = (runiform() > 0.5)
    end

    cap prog drop testMSE
    prog def testMSE
        preserve
        gen testMSE = unemployment_rate-yhat
        replace testMSE = (testMSE*testMSE)/df
        collapse (sum) testMSE
        scalar MSE = sqrt(testMSE[1])
        restore
    end
    """
)


# Model 1 - Naive Federal Reserve Minutes (Top 10 words)
# Unemployment ~ State + (Year * Month) + χ(FedKeywords) + ε
Macro.setGlobal('keywords', " ".join(fed[:3]))
stata.run(
    """
    configStata
    splitData, seed(101)

    xtreg unemployment_rate i.year##i.month $keywords if train, fe vce(robust)
    scalar df = e(df_r)
    predict yhat if !train
    testMSE
    """
)

# Model 2 - LASSO Selected Federal Reserve Minutes
# Unemployment ~ State + (Year * Month) + χ(FedKeywords) + ε
Macro.setGlobal('keywords', " ".join(fed[:3]))
stata.run(
    """
    configStata
    splitData, seed(101)

    xtreg unemployment_rate i.year##i.month $keywords if train, fe vce(robust)
    scalar df = e(df_r)
    predict yhat if !train
    testMSE
    """
)

# Model 3 - LASSO Selected Federal Reserve Minutes & 1/2 Month Lags, no Time FEs
# Unemployment ~ L1.Unemployment + L2.Unemployment + State + χ(FedKeywords) + ε
Macro.setGlobal('keywords', " ".join(fed[:3]))
stata.run(
    """
    configStata
    splitData, seed(101)

    xtreg unemployment_rate i.year##i.month $keywords if train, fe vce(robust)
    scalar df = e(df_r)
    predict yhat if !train
    testMSE
    """
)
stata.run('line unemployment_rate yhat lag if stname=="Alaska", sort', echo=True)
stata.run("graph export did1.png, replace", quietly=True)
# LASSO Shakespeare
# Literature inspired (1-3 models, Model 0)
#
