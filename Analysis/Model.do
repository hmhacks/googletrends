/*
Basic Fixed effect regression. 
*/

clear all
use "unemploymentMaster", clear

*Create lag/lead variables for search term. lag_unemployment ==. won't be regressed
sort state year month 
gen lag_unemployment = . 
replace lag_unemployment = gunemployment[_n+1] if fips[_n-1] == fips[_n]

gen lead_unemployment = .
replace lead_unemployment = gunemployment[_n-1] if fips[_n-1] == fips[_n]
order lead_unemployment lag_unemployment gunemployment

//// Aggregate two-way fixed effects: 'unemployment'////
xtset fips date
xtreg unemployment_rate i.year i.month gunemployment, fe vce(robust)

*Training runiform()
set seed 123
cap drop train yhat
gen train = (runiform() > 0.5)
xtreg unemployment_rate i.year i.month gunemployment if train, fe vce(robust) 
scalar df = e(df_r)
predict yhat if !train

preserve /// Test MSE. Reuse this code to compare models
gen testMSE = unemployment_rate - yhat
replace testMSE = (testMSE*testMSE)/df
collapse (sum) testMSE
scalar MSE = sqrt(testMSE[1])
restore

	* Visualize
	line unemployment_rate yhat date if stname==`"New York"', sort
	line unemployment_rate yhat date if stname=="Virginia", sort
	line unemployment_rate yhat date if stname=="Maine", sort
	line unemployment_rate yhat date if stname=="Wyoming", sort

*Training (2008 > train < 2016, 2019 > test > 2016)
cap drop train yhat
gen train = 0 
replace train = 1 if year < 2016
xtreg unemployment_rate i.year i.month gunemployment if train, fe vce(robust)
predict yhat if !train 

	* Visualize
	line unemployment_rate yhat date if stname=="California", sort
	line unemployment_rate yhat date if stname=="Virginia", sort
	line unemployment_rate yhat date if stname=="Maine", sort
	line unemployment_rate yhat date if stname=="Wyoming", sort
	
	
	
//// Aggregate two-way fixed effects with 1 mo.lag/leads: 'unemployment'////

*Lag
cap drop train yhat
gen train = (runiform() > 0.5)
xtreg unemployment_rate i.year i.month lag_unemployment if train, fe vce(robust) 
predict ylaghat if !train

*Lead
xtreg unemployment_rate i.year i.month lead_unemployment if train, fe vce(robust) 
predict yleadhat if !train

*None
xtreg unemployment_rate i.year i.month gunemployment if train, fe vce(robust) 
predict yhat if !train

* Visualize
	line unemployment_rate yhat ylaghat yleadhat date if stname=="California", sort
	line unemployment_rate yhat ylaghat yleadhat date if stname=="Virginia", sort
	line unemployment_rate yhat ylaghat yleadhat date if  stname=="Maine", sort
	line unemployment_rate yhat ylaghat yleadhat date if  stname=="Wyoming", sort

//// Aggregate two-way fixed effects: 'unemployment', 'google flights'////

