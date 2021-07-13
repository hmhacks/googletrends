/*

Henry Manley - hjm67@cornell.edu
7/12/2021

*/

scalar installed = 1
if installed == 0 {
	ssc install rforest
}

cap prog drop buildData
prog def buildData
	use "/$data/workingData", clear

	clear mata
	clear matrix
	set seed 201807
	splitData, year(2016)
end


*******************************************************************************
********************** Random Forest Regression *******************************
*******************************************************************************

* Helper(s)
cap prog drop visualize 
prog def visualize
	syntax, series(string) x(string)
	levelsof state, loc(states)
	loc accum = ""
	loc i = 1
	foreach state in `states'{
		gen `series'`i' = `series' if state  == "`state'"
		loc accum = `"`accum' `series'`i'"'
		loc ++ i
	}
	gr two ///
	(line `accum' `x', legend(off) mlabel(state)), ///
	graphregion(color(white)) plotregion(color(white)) ///
	xtitle("`x'") ytitle("Error") title("`series' By State, Iterations", color(black))
end 

cap prog drop randomForest 
prog def randomForest
	buildData
	ds *_d 
	local dlist = r(varlist)
	local not unemployment_rate_d *_lag_*
	local dlist: list dlist- not
	di "`dlist'"
	
	preserve 
	keep in 1 
	tempfile results
	save `results', replace
	restore 


	* Number of iterations
	levelsof state, loc(states)
	foreach state in `states'{
		di "`state'"
		
		forval i = 5(20)245 {
			nois di "`i'"
			qui{	
				
				rforest unemployment_rate_d month_year `dlist' ///
				if state == "`state'" & train, type(reg) iter(`i') numvars(1)
				
				preserve
				predict prf if test
				gen iter = `i'
				gen validation_rmse = `e(RMSE)' if state == "`state'" 
				gen oob_err = `e(OOB_Error)' if state == "`state'"
				drop prf
				keep if validation_rmse != .
				keep in 1
				append using `results'
				save `results', replace
				restore

			}
		}
	}

	use `results', clear
	keep state validation_rmse oob_err iter
	count 
	drop in `r(N)'

	visualize, series("validation_rmse") x("iter")
	visualize, series("oob_err") x("iter")

	use `results', clear
	keep in 1 
	save `results', replace


	* Number of features
	buildData
	ds *_d 
	local dlist = r(varlist)
	local not unemployment_rate_d *_lag_*
	local dlist: list dlist- not
	di "`dlist'"
	
	local total `: word count `dlist''
	foreach state in `states'{
		di "`state'"
		forval i = 1/`total'{
			nois di "`i'"
			qui{	
				
				rforest unemployment_rate_d month_year `dlist' ///
				if state == "`state'" & train, type(reg) iter(50) numvars(`i')
				
				preserve
				predict prf if test
				gen vars = `i'
				gen validation_rmse = `e(RMSE)' if state == "`state'" 
				gen oob_err = `e(OOB_Error)' if state == "`state'"
				drop prf
				keep if validation_rmse != .
				keep in 1
				append using `results'
				save `results', replace
				restore

			}
		}

	}

	use `results', replace
	keep state validation_rmse oob_err vars
	count 
	drop in `r(N)'

	visualize, series("validation_rmse") x("vars")
	visualize, series("oob_err") x("vars")

end

*******************************************************************************
************************** LASSO Regression ***********************************
*******************************************************************************

cap prog drop LASSOreg
prog def LASSOreg
	buildData
	ds *_d 
	local dlist = r(varlist)
	local not unemployment_rate_d *_lag_*
	local dlist: list dlist- not
	di "`dlist'"

	lasso linear unemployment_rate_d month `dlist'
	lassocoef
	ret li

	local predictors: rownames r(coef)[]
	local remove _cons
	local predictors: list predictors - remove
	xtset fips 
	xtreg unemployment_rate `predictors' if train, fe vce(robust)

	scalar df = e(df_r)
	predict yhat if !train
	testRMSE, outcome("unemployment_rate_d") state("New York")
	loc RMSE = RMSE

	line unemployment_rate yhat date if state=="New York", sort ///
	caption("RMSE = `RMSE'")

end

// LASSOreg

*******************************************************************************
********************** Autoregressive Regression ******************************
*******************************************************************************
cap prog drop ARreg
prog def ARregreg
buildData
ds *_d 
local dlist = r(varlist)
local not unemployment_rate_d *_lag_*
local dlist: list dlist- not

sort fips month_year
forval i = 1/5{
	by fips: gen unemployment_lead_`i' = unemployment_rate[_n+`i']
}

gen unemployment_lead_0 = unemployment_rate_d

xtset fips
forval i = 0/5{
	xtreg unemployment_lead_`i' unemployment_lag_1 unemployment_lag_2, fe vce(robust)
	scalar df = e(df_r)
	predict yhat`i'
   
}

line unemployment_lead_1 yhat1 date if state=="California", sort ///
	graphregion(color(white)) plotregion(color(white)) ///
	title("Autoregressive Forecasting U3")
end
