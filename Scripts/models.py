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
    sleep 5

    gen date = month + "/" + year
	gen date1 = date(date, "MY")
    drop date
    rename date1 date

	sort state date
	format date %td

	ds
	local vlist = r(varlist)
	foreach y of local vlist{
		cap destring `y', replace
	}

	duplicates drop month year fips, force

	save "/$data/unemploymentMaster", replace

	merge 1:1 month year fips using `working', force
	keep if _me ==3
    drop _me

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
        cap drop train
        cap drop yhat
        cap drop lag*
        set seed `seed'
        cap drop train yhat
        gen train = (runiform() > 0.5)

        *Date after
        *gen train = (date > )
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
Macro.setGlobal('keywords', " ".join(pyStrToStaLoc(fed)))
stata.run(
    """
    configStata
    splitData, seed(101)

    xtreg unemployment_rate i.year##i.month $keywords if train, fe vce(robust)
    scalar df = e(df_r)
    predict yhat if !train
    testMSE

    line unemployment_rate yhat date if stname=="California", sort
    graph export model1.png, replace
    """
)

# Model 2 - LASSO Selected Federal Reserve Minutes
# Unemployment ~ State + (Year * Month) + χ(FedKeywords) + ε
Macro.setGlobal('keywords', " ".join(pyStrToStaLoc(fed)))
stata.run(
    """
    configStata
    splitData, seed(101)

    lasso linear unemployment_rate $keywords (i.year##i.month) if train
    lassocoef
    ret li

    local predictors: rownames r(coef)[]
    local remove _cons
    local predictors: list predictors - remove
    xtreg unemployment_rate `predictors' if train, fe vce(robust)

    scalar df = e(df_r)
    predict yhat if !train
    testMSE

    line unemployment_rate yhat date if stname=="California", sort
    graph export model2.png, replace
    """
)

# Model 3 - LASSO Selected Federal Reserve Minutes & 1/2 Month Lags, no Time FEs
# Unemployment ~ L1.Unemployment + L2.Unemployment + State + χ(FedKeywords) + ε
Macro.setGlobal('keywords', " ".join(pyStrToStaLoc(fed)))
stata.run(
    """
    configStata
    splitData, seed(101)

    sort fips year month
    by fips: gen lag1 = unemployment_rate[_n-1]
    by fips: gen lag2 = unemployment_rate[_n-2]

    list in 1/4

    lasso linear unemployment_rate $keywords (lag1 lag2 i.year##i.month) if train
    lassocoef
    ret li

    local predictors: rownames r(coef)
    local remove _cons
    local predictors: list predictors - remove
    xtreg unemployment_rate `predictors' if train, fe vce(robust)

    scalar df = e(df_r)
    predict yhat if !train
    testMSE

    line unemployment_rate yhat date if stname=="California", sort
    graph export model3.png, replace
    """
)


# Model 4 - D'Amuri2017 Autoregressive model
# Unemployment ~ L1.Unemployment + L2.Unemployment + State + χ(Keywords) + ε
Macro.setGlobal('keywords', " ".join(fed))
stata.run(
    """
    configStata
    * splitData, seed(101)
    sort fips year month
    cap drop lag*
    cap drop lead*

    forval i = 1/5{
        by fips: gen lag`i' = unemployment_rate[_n-`i']
    }

    forval i = 1/5{
        by fips: gen lead`i' = unemployment_rate[_n+`i']
    }
    gen lead0 = unemployment_rate

    forval i = 0/5{
        xtreg lead`i' lag1 lag2 $keywords, fe vce(robust)
        scalar df = e(df_r)
        predict yhat`i'
        *testMSE
    }
    line unemployment_rate yhat* date if stname=="California", sort ///
        graphregion(color(white)) plotregion(color(white)) ///
        title("Autoregressive Forecasting U3")
    graph export model4.png, replace
    """
)
