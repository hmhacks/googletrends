
import delimited "/Users/henrymanley/Downloads/bf1acd2290e15b91e6710b6fd3be0a53-11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv", clear
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

save "unemploymentMaster", replace

merge 1:1 month year fips using `working', force


keep if _me ==3
export delimited using "/Users/henrymanley/Desktop/Research/googletrends/Data/workingData", replace


set graphics off
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"

sort stname
// levelsof stname, local(st_list)
local st_list = `" "Alabama" "Texas" "Florida" "Illinois" "California" "'
local terms = "spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay google_unemployment slutload calvinklein"

	foreach sta of local st_list{
		foreach term of local terms {
			regress unemployment_rate `term' if stname == "`sta'", robust
			predict `term'_p_`sta'
			local r2 = round(`e(r2)', 0.001)


			twoway ///
				(lpolyci unemployment_rate `term' if stname == "`sta'", degree(3) kernel(epan2)) ///
				(scatter unemployment_rate `term' if stname == "`sta'") ///
				(line `term'_p_`sta' `term' if stname == "`sta'", title("`sta' Monthly Google Search for '`term'' vs. EPOP Rate", size(medium)) xtitle("Google Searches for "`term'"") ytitle("EPOP") caption("R2 Linear = `r2'") graphregion(color(white)) plotregion(color(white)) legend(label(1 "Nonparametric CI") label(2 "Nonparametric") label(3 "") label(4 "Linear")))


			graph export "$images/`sta'_`term'_goog.png", replace height(350) width(500)

		}
	}


cd "$images"
putpdf begin
	putpdf paragraph

	foreach sta of local st_list{
		foreach term of local terms {
				putpdf image "$images/`sta'_`term'_goog.png"
		}

}
	putpdf save "$images/Controls.pdf", replace


foreach sta of local st_list{
		foreach term of local terms {
			erase  "$images/`sta'_`term'_goog.png"
		}
}





	pca spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay google_unemployment slutload


*identify different states where "unemployment" does predict!
*proof of concept
*initial claims?
*ICSA in Fred
*lets do the next round --> by state, just "unemployment"
