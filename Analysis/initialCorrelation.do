import delimited "/Users/henrymanley/Downloads/bf1acd2290e15b91e6710b6fd3be0a53-11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv", clear 
rename stusps state 
replace state = subinstr(state, " ","",.)
tempfile working
save `working',replace

import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/SearchTerms/unemployment.csv", encoding(UTF-8) clear 
gen month = substr(date, 6,2)
gen year = substr(date,1, 4)
destring month, replace
destring year, replace
merge m:1 state using `working'
drop _me 
rename unemployment google_unemployment
rename st fips

***
*by month calculations
sort state year month
by state year month: egen groupmean=mean(google_unemployment)
duplicates drop month year fips, force
***


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

set graphics off
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"

sort stname
levelsof stname, local(st_list)

qui{
	foreach sta of local st_list{
	cap drop x
	regress unemployment_rate google_unemployment if stname == "`sta'"
	local r2 = `e(r2)'
	predict x
	
	twoway ///
		(scatter unemployment_rate google_unemployment if stname == "`sta'") ///
		(line x google_unemployment, title("`sta' Monthly Google Search for 'Unemployment' vs. EPOP Rate", size(medium)) legend(off) xtitle("Google Searches for 'Unemployment'") ytitle("EPOP") caption("R2 = `r2'") graphregion(color(white)) plotregion(color(white))) ///
		(lpoly unemployment_rate google_unemployment)
		
		graph export "$images/`sta'_goog1.png", replace height(350) width(500)

	twoway ///
		(scatter unemployment_rate date if stname == "`sta'") ///
		(scatter google_unemployment date if stname == "`sta'", title("`sta' Trends Over Time") graphregion(color(white)) plotregion(color(white)))
		graph export "$images/`sta'_goog2.png", replace height(350) width(500)
}
}



cd "$images"
putpdf begin
	putpdf paragraph
	levelsof stname, local(st_list)

	foreach sta of local st_list{
		putpdf image "$images/`sta'_goog1.png"
		putpdf image "$images/`sta'_goog2.png"
}
		
	
	putpdf save "$images/noControls.pdf", replace
	
	
	
	
	
