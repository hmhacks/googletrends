/*
FWL analysis.
*/

clear all

global analysis "/Users/henrymanley/Desktop/Research/googletrends/Analysis"
cd "$analysis"
do dataBuild

set graphics off
global data "/Users/henrymanley/Desktop/Research/googletrends/Data"
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"
use "$data/unemploymentMaster", clear

* Relative unemployment
drop date
drop if state =="District of Columbia" | state == "Los Angeles County"
gen rel_unemployment = 0
levelsof state, loc(states)
loc states = `" `states' "'
foreach state in `states'{
	di "`state'"
	summ unemployment_rate if state == "`state'"
	replace rel_unemployment = 100* unemployment_rate/`r(max)' if state =="`state'"
}

rename lag date
* Calculate residuals
reg rel_unemployment date i.year i.month i.fips, robust
predict resY, residuals

reg gunemployment date i.year i.month i.fips, robust
predict resX, residuals

*Compresses the PDF
putpdf begin
putpdf paragraph, font("Garamond",20) halign(center)

set graphics off
// levelsof state, loc(states)
foreach state in `states'{
	noisily di "`state'"
	qui {
		* Plot residuals
		gr tw scatter resY resX date if state =="`state'", ///
			graphregion(color(white)) plotregion(color(white)) ///
			xtitle("Time")  ytitle("Residualized Rate") title("Residuals", color(black)) ///
			msymbol(o o) msize(small small) mcolor(black red) xlabel(, alternate) ///
			legend(cols(1) region(lstyle(none)) label(1 "Rel. Unemployment Rate x FE") label(2 "G-Unemployment x FE"))
			gr save "residuals_`state'.gph", replace
			
		gr tw scatter rel_unemployment gunemployment date if state =="`state'", ///
			graphregion(color(white)) plotregion(color(white))  ///
			xtitle("Time")  ytitle("Rate") title("Time Series", color(black)) ///
			msymbol(o o) msize(small small) mcolor(black red) xlabel(, alternate) ///
			legend(cols(1) region(lstyle(none)) label(1 "Rel. Unemployment Rate") label(2 "G-Unemployment"))
			gr save "timeseries_`state'.gph", replace
			
		gr combine "timeseries_`state'" "residuals_`state'", ///
			title("Residualized Estimates v. Time Series - `state'", color(black)) ///
			graphregion(color(white)) plotregion(color(white))
			gr export "timeseries_`state'.png"
			
		putpdf image "timeseries_`state'.png"
		putpdf paragraph
		
		erase "timeseries_`state'.png"
		erase "timeseries_`state'.gph"
		erase "residuals_`state'.gph"
	}
}

putpdf save "$images/FWL.pdf", replace
*make unemployment relative and then graph
*every other on x axis 
* iterate through each state and compress new pdf
* keep writing a bit --> more literature analysis
