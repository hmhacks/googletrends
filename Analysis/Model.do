/*
Basic Fixed effect regression. 
*/

clear all

global analysis "/Users/henrymanley/Desktop/Research/googletrends/Analysis"
cd "$analysis"
do dataBuild

set graphics off
global data "/Users/henrymanley/Desktop/Research/googletrends/Data"
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"
use "$data/unemploymentMaster", clear
xtset fips

*Create lag/lead variables for search term. lag_unemployment ==. won't be regressed
sort state year month 
gen lag_unemployment = . 
replace lag_unemployment = gunemployment[_n+1] if fips[_n-1] == fips[_n]

gen lead_unemployment = .
replace lead_unemployment = gunemployment[_n-1] if fips[_n-1] == fips[_n]
order lead_unemployment lag_unemployment gunemployment

////////////////////////////////////////////////////////////////////////////
//// Aggregate two-way fixed effects: 'unemployment'////////////////////////
////////////////////////////////////////////////////////////////////////////

xtreg unemployment_rate i.year i.month gunemployment, fe vce(robust)

*Training runiform()
set seed 123
cap drop train yhat
gen train = (runiform() > 0.5)
xtreg unemployment_rate i.year i.month gunemployment if train, fe vce(robust) 
scalar df = e(df_r)
predict yhat if !train

preserve 
gen testMSE = unemployment_rate-yhat
replace testMSE = (testMSE*testMSE)/df
collapse (sum) testMSE
scalar MSE = sqrt(testMSE[1])
restore

	* Visualize
// 	line unemployment_rate yhat date if stname==`"New York"', sort
// 	line unemployment_rate yhat date if stname=="Virginia", sort
// 	line unemployment_rate yhat date if stname=="Maine", sort
// 	line unemployment_rate yhat date if stname=="Wyoming", sort

*Training (2008 > train < 2017, 2017 > test > 2016)
cap drop train yhat
gen train = 0 
replace train = 1 if year < 2017
xtreg unemployment_rate i.year i.month gunemployment if train, fe vce(robust)
predict yhat if !train 

	* Visualize
// 	line unemployment_rate yhat date if stname=="California", sort
// 	line unemployment_rate yhat date if stname=="Virginia", sort
// 	line unemployment_rate yhat date if stname=="Maine", sort
// 	line unemployment_rate yhat date if stname=="Wyoming", sort
	
	
////////////////////////////////////////////////////////////////////////////	
//// Aggregate two-way fixed effects with 1 mo.lag/leads: 'unemployment'////
////////////////////////////////////////////////////////////////////////////

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
// 	line unemployment_rate yhat ylaghat yleadhat date if stname=="California", sort
// 	line unemployment_rate yhat ylaghat yleadhat date if stname=="Virginia", sort
// 	line unemployment_rate yhat ylaghat yleadhat date if  stname=="Maine", sort
// 	line unemployment_rate yhat ylaghat yleadhat date if  stname=="Wyoming", sort

	
////////////////////////////////////////////////////////////////////////////	
//// dy/dx: Change in unemployment rate vs. change in google searches //////
////////////////////////////////////////////////////////////////////////////	
*Note, this is more of a classifcation question. Will the unemployment rate, in 
* weeks go up, down, or stay the same??
sort fips
* change in 'unemployment'
gen deltaGunemployment = gunemployment[_n] - gunemployment[_n-1] & fips[_n-1] == fips[_n]
gen deltaGunemploymentUp = 0
replace deltaGunemploymentUp = 1 if deltaGunemployment > 0 

* change in 'unemployment'
gen deltaFlights = googleflights[_n] - googleflights[_n-1] & fips[_n-1] == fips[_n]
gen deltaFlightsUp = 0
replace  deltaFlightsUp =  1 if deltaFlights < 0 

* change in unemployment rate
gen deltaY = unemployment_rate[_n] - unemployment_rate[_n-1]
gen deltaYUp = 0 
replace deltaYUp = 1 if deltaY > 0 
	
////////////////////////////////////////////////////////////////////////////
//// Aggregate two-way fixed effects: 'unemployment', 'google flights'//////
////////////////////////////////////////////////////////////////////////////
cap drop train yhat
gen train = 0 
replace train = 1 if year < 2017
xtreg unemployment_rate i.year i.month gunemployment googleflights if train, fe vce(robust) 
scalar df = e(df_r)
predict yhat if !train

preserve 
gen testMSE = unemployment_rate-yhat
replace testMSE = (testMSE*testMSE)/df
collapse (sum) testMSE
scalar MSE = sqrt(testMSE[1])
restore

	* Visualize
// 	line unemployment_rate yhat date if stname==`"New York"', sort
// 	line unemployment_rate yhat date if stname==`"New Jersey"', sort
// 	line unemployment_rate yhat date if stname=="Virginia", sort
// 	line unemployment_rate yhat date if stname=="Maine", sort
// 	line unemployment_rate yhat date if stname=="Wyoming", sort
// 	line unemployment_rate yhat date if stname=="California", sort
// 	line unemployment_rate yhat date if stname=="Texas", sort
// 	line unemployment_rate yhat date if stname==`"Illinois"', sort
	
////////////////////////////////////////////////////////////////////////////
// Two-way fixed effects: 'unemployment', 'google flights', 'pornhub'///////
////////////////////////////////////////////////////////////////////////////	
cap drop train yhat
gen train = (runiform() > 0.5)
xtreg unemployment_rate i.year i.month gunemployment googleflights pornhub if train, fe vce(robust) 
scalar df = e(df_r)
predict yhat if !train

* Calculate testMSE by state, creates matrix MSE
preserve
gen residual = unemployment_rate-yhat
gen residualsquared = residual*residual
gen id = 1
collapse (sum) residualsquared id, by(state)
gen MSE = residualsquared/id
mkmat MSE, matrix(MSE)
levelsof(state), local(rnames)
mat rownames MSE = 	`rnames'
restore


	* Visualize
// 	line unemployment_rate yhat date if stname==`"New York"', sort
// 	line unemployment_rate yhat date if stname==`"New Jersey"', sort
// 	line unemployment_rate yhat date if stname=="Virginia", sort
// 	line unemployment_rate yhat date if stname=="Maine", sort
// 	line unemployment_rate yhat date if stname=="Wyoming", sort
// 	line unemployment_rate yhat date if stname=="California", sort
// 	line unemployment_rate yhat date if stname=="Texas", sort
// 	line unemployment_rate yhat date if stname=="Colorado", sort
// 	line unemployment_rate yhat date if stname==`"Illinois"', sort
	
	levelsof stname, local(states)
	loc j = 1
	
	qui foreach sta of local states {
		local MSE = MSE[`j', 1]
		line unemployment_rate yhat date if stname==`"`sta'"', sort title(`"`sta'"') caption("Test MSE = `MSE'")
		
		graph export "$images/`sta'_prediction.png", replace height(350) width(500)
		loc j = `j' + 1
	}

	putpdf begin
	putpdf table tb= matrix(MSE), rownames
	putpdf pagebreak
	putpdf paragraph, font("Garamond",20) halign(center)

	foreach sta of local states{
		putpdf paragraph
		cap putpdf image "$images/`sta'_prediction.png"
	}
	putpdf save "$images/predictions.pdf", replace


	foreach sta of local states{
			cap erase  "$images/`sta'_prediction.png"
	}


	
	
