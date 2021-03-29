/*
This script returns a compressed pdf with user defined state/keyword scatter plots
and time series. Namely, this file helps to visualize regressors.

ControlInteractions
*/

clear all
global data "/Users/henrymanley/Desktop/Research/googletrends/Data"
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"
local terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay gunemployment slutload calvinklein"

local st_list = `" "California" "'

****


*Builds the necessary dataset to visualize regressors
import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/statefips.csv", clear
rename stusps state
replace state = subinstr(state, " ","",.)
tempfile working
save `working',replace

import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/allSearchTerms.csv", encoding(UTF-8) clear
gen month = substr(date, 6,2)
gen year = substr(date,1, 4)
destring month, replace
destring year, replace
merge m:1 state using `working'
drop _me
rename unemployment google_unemployment
rename st fips

*Smooth the time series (if needed)
// ***
// *by month calculations
// sort state year month
// by state year month: egen groupmean=mean(google_unemployment)
// duplicates drop month year fips, force
// ***

save `working', replace

import excel "/Users/henrymanley/Desktop/Research/googletrends/TESTING.xlsx", sheet("ststdsadata") clear
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
format date1 %td
drop date
rename date1 date


ds
local vlist = r(varlist)
foreach y of local vlist{
	cap destring `y', replace
}
duplicates drop month year fips, force

save "/$data/unemploymentMaster", replace

merge 1:1 month year fips using `working', force
keep if _me ==3

rename google_unemployment gunemployment


*Generates interaction terms

// foreach term1 of local terms {
// 	foreach term2 of local terms {
// 		if `term1' != `term2' {
// 			gen `term1'_`term2' = sqrt(`term1' * `term2')
// 		}
// 	}
// }

save "/$data/unemploymentMaster", replace



export delimited using "/Users/henrymanley/Desktop/Research/googletrends/Data/workingData", replace
set graphics off


program define StateTimeScatters

local terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay gunemployment slutload calvinklein"

local st_list = `" "California" "'

*Generates state level scatter plots
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"

sort stname
// levelsof stname, local(st_list)


gen rel_unemployment = 0
foreach sta of local st_list{
summ unemployment_rate if stname == "`sta'"
replace rel_unemployment = 100* unemployment_rate/`r(max)' if stname =="`sta'"
}

foreach sta of local st_list{
		scatter rel_unemployment googleflights gunemployment slutload date if stname=="`sta'", ///
		graphregion(color(white)) plotregion(color(white)) ///
		title("`sta' Time Series. Relative Unemployment and Google Searches 2011 - 2019", size(medium))
		graph export "$images/`sta'_timeSeries.png", replace height(350) width(500)
}


foreach sta of local st_list{
	foreach term of local terms {
		regress unemployment_rate `term' if stname == "`sta'", robust
		predict `term'_p_`sta'
		local r2 = round(`e(r2)', 0.001)


		twoway ///
			(lpolyci unemployment_rate `term' if stname == "`sta'", degree(3) kernel(epan2)) ///
			(scatter unemployment_rate `term' if stname == "`sta'") ///
			(line `term'_p_`sta' `term' if stname == "`sta'", ///
				title("`sta' Monthly Google Search for '`term'' vs. EPOP Rate", size(medium)) ///
				xtitle("Google Searches for "`term'"") ytitle("EPOP") caption("R2 Linear = `r2'") ///
				graphregion(color(white)) plotregion(color(white)) ///
				legend(label(1 "Nonparametric CI") label(2 "Nonparametric") ///
				label(3 "") label(4 "Linear")))

		graph export "$images/`sta'_`term'_goog.png", replace height(350) width(500)

		}
	}


*Compresses the PDF
cd "$images"
putpdf begin
	putpdf paragraph, font("Garamond",20) halign(center)

	foreach sta of local st_list{
		putpdf text ("`sta'")
		putpdf pagebreak
		putpdf paragraph
		putpdf image "$images/`sta'_timeSeries.png",
		foreach term of local terms {
				putpdf image "$images/`sta'_`term'_goog.png"
		}

}
	putpdf save "$images/Controls.pdf", replace


*Erases all local images
foreach sta of local st_list{
		foreach term of local terms {
			erase  "$images/`sta'_`term'_goog.png"
		}
}
end




local terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay gunemployment slutload calvinklein"

local st_list = `" "California" "'

use "unemploymentMaster", clear
*Visualizing the interaction terms
foreach sta of local st_list {
	foreach term1 of local terms {
		foreach term2 of local terms {

			if `term1' != `term2' {
				
				regress unemployment_rate `term1'_`term2' if stname == "`sta'", robust
				local name = "`term1'`term2'`sta'"
				predict `name'

				local r2 = round(`e(r2)', 0.001)
				
				twoway ///
					(lpolyci unemployment_rate `term1'_`term2' if stname == "`sta'", degree(3) kernel(epan2)) ///
					(scatter unemployment_rate `term1'_`term2' if stname == "`sta'") ///
					(line `name' `term1'_`term2' if stname == "`sta'", ///
						title("`sta' Monthly Google Search for '`term1'_`term2'' vs. EPOP Rate", ///
						size(medium)) xtitle("Google Searches for "`term1'_`term2'"") ytitle("EPOP") ///
						caption("R2 Linear = `r2'") graphregion(color(white)) plotregion(color(white)) ///
						legend(label(1 "Nonparametric CI") label(2 "Nonparametric") ///
						label(3 "") label(4 "Linear")))
				graph export "$images/`sta'`term1'`term2'goog.png", replace
				
			}
		}
	}
}

local terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay gunemployment slutload calvinklein"

local st_list = `" "California" "'
*Compresses the PDF
cd "$images"
putpdf begin
	putpdf paragraph, font("Garamond",20) halign(center)

	foreach sta of local st_list{
		putpdf text ("`sta'")
		putpdf pagebreak
		putpdf paragraph
		foreach term1 of local terms {
			foreach term2 of local terms {
				cap putpdf image "$images/`sta'`term1'`term2'goog.png"
		}
	}
}
	putpdf save "$images/interactionControls.pdf", replace


*Erases all local images
foreach sta of local st_list{
		foreach term1 of local terms {
			foreach term2 of local terms {
					cap erase  "$images/`sta'`term1'`term2'goog.png"
		}
	}
}



// 	pca spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay google_unemployment slutload
