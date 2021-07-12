/*

Henry Manley - hjm67@cornell.edu
7/12/2021

This file collects all relevant local data files and combines them to 
produce an analysis-ready dataset. The Recursive Augmented Dickey Fuller Test 
(RADF) is performed to evidence a need to compute first differences in both 
the outcome of interest (state-level unemployment rate) but also Google-Trends 
based predictive features.

*/

global data "/Users/henrymanley/desktop/research/googletrends/data"
global analysis "/Users/henrymanley/desktop/research/googletrends/analysis"

*******************************************************************************
********************* Merging and Cleaning all Data ***************************
*******************************************************************************

* State fips
import delimited "$data/statefips.csv", clear
rename stusps state
replace state = subinstr(state, " ","",.)
tempfile working
save `working',replace

* Search Terms
import delimited "$data/SearchTerms/MASTERDATA", clear
tostring date, replace
gen month = substr(date, 5,2)
gen year = substr(date,1, 4)
destring month, replace
destring year, replace
merge m:1 state using `working'
drop _me
rename st fips
save `working', replace

* Unemployment Panel
import excel "$data/BLS/unemploymentPanelBLS.xlsx", sheet("ststdsadata") clear
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

save "/$data/unemploymentMaster", replace
duplicates drop fips year month, force
merge 1:1 month year fips using `working', force
keep if _me ==3
drop _me
egen month_year = group(year month)
drop civ_pop* employed unemployed percent* v1 stname
order state fips year month month_year date unemployment_rate
local houseKeepingVars state fips year month month_year date unemployment_rate

save "/$data/workingData", replace

*******************************************************************************
**************** Defining Helper Functions for models.do **********************
*******************************************************************************

cap prog drop configStata
prog def configStata
	cd "$analysis"
	set graphics on
	xtset fips
	tsset month_year
end


cap prog drop splitData
prog def splitData
	syntax, year(integer)
	cap drop train
	cap drop yhat
	cap drop train yhat
	gen train = (year < `year')
	gen test = !train
end

cap prog drop testRMSE
prog def testRMSE
	syntax, outcome(string) [state(string)]
	preserve

	if "`state'"!= ""{
		gen testMSE = `outcome'-yhat if state == "`state'"
		count if state == "`state'"
		replace testMSE = (testMSE*testMSE)/r(N)
	}
	else {
		gen testMSE = `outcome'-yhat
		replace testMSE = (testMSE*testMSE)/_N
	}

	collapse (sum) testMSE
	scalar RMSE = sqrt(testMSE[1])
	restore
end


*******************************************************************************
************* Performing Recursive Augmented Dickey Fuller ********************
*******************************************************************************

cap prog drop augDickeyFuller
prog def augDickeyFuller
  syntax varlist
  tsset month_year
  foreach var in `varlist'{
    dfuller `var', lags(1) trend
  }
end

use "/$data/workingData", clear

local houseKeepingVars state fips year month month_year date unemployment_rate
ds
local vlist = r(varlist)
local total `: word count `vlist''
local subset `: word count `houseKeepingVars''

di `total'-`subset'
local numberFeatures = (`total' - `subset') * 50
di `numberFeatures'

loc pCount = 0
levelsof state, loc(states)
foreach state in `states'{
	preserve 
	di "`state'"
	keep if state == "`state'"
	foreach var in `vlist'{
		if `: list var in houseKeepingVars' continue 
		drop if `var' == .
		if _N < 2 continue
		else qui augDickeyFuller `var'
		ret li
		
		if `r(p)' > 0.05 loc ++pCount
	}
	restore
}

nois di "`pCount' of `numberFeatures' total state-features fail to RADF reject null."

loc pCount = 0
loc iterations = 0
foreach state in `states'{
	loc ++iterations
	preserve 
	keep if state == "`state'"
	qui augDickeyFuller unemployment_rate
	ret li
	if `r(p)' > 0.05 loc ++pCount
	restore
}

nois di "`pCount' of `iterations' states fail to RADF reject null for unemployment_rate."

*******************************************************************************
********************** Computing First Differences ****************************
*******************************************************************************
sort state month_year
foreach state in `states'{
	cap gen unemployment_rate_d= unemployment_rate[_n] - unemployment_rate[_n-1] if state == "`state'"
	replace unemployment_rate_d = . if month_year == 1
	cap replace unemployment_rate_d = unemployment_rate[_n] - unemployment_rate[_n-1] if state == "`state'"	
	foreach var in `vlist'{
		if `: list var in houseKeepingVars' continue 
		cap gen `var'_d = `var'[_n] - `var'[_n-1] if state == "`state'"	
		cap replace `var'_d = `var'[_n] - `var'[_n-1] if state == "`state'"	
	}
}

ds *_d
local dlist = r(varlist)
ds 
local allList = r(varlist)

foreach var in `allList'{
	if `: list var in dlist' continue 
	if `: list var in houseKeepingVars' continue 
	drop `var'
}
drop unemployment_rate

ds
foreach var in `vlist'{
	if `: list var in houseKeepingVars' continue 
	di "`var'"
	qui count if `var' == .
	qui if r(N)/_N > 0.5 drop `var'
}
drop if unemployment_rate_d == .

*******************************************************************************
****************************** Create Lags ************************************
*******************************************************************************

preserve 
keep in 1 
tempfile localData
save `localData', replace
restore

levelsof state, loc(states)
sort state month_year
foreach state in `states'{
	preserve
	keep if state == "`state'"
	forval i = 1/12{
		gen unemployment_lag_`i' = unemployment_rate_d[_n - `i'] 
	}
	append using `localData'
	save `localData', replace
	restore 
}

use `localData', clear
drop in 1

save "/$data/workingData", replace 

