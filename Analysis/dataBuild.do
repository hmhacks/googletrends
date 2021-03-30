/*
Converts and merges all data into a .dta for analysis.
*/

di "Building data from local csv's...'"
qui{
		
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
	}
