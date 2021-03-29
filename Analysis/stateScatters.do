/*
Generates state/term time series plots. Returns compressed pdf with embedded pngs
*/

clear all
set graphics off
global data "/Users/henrymanley/Desktop/Research/googletrends/Data"
global images "/Users/henrymanley/Desktop/Research/googletrends/Images"

cd "$data"
use "unemploymentMaster", clear

drop if state =="Los Angeles County"
levelsof state, local(states)


gen rel_unemployment = 0
foreach sta of local states{
	di "`sta'"
	summ unemployment_rate if stname == "`sta'"
	replace rel_unemployment = 100* unemployment_rate/`r(max)' if stname =="`sta'"
}

tempfile data
save `data', replace

qui foreach sta of local states{
	use `data', clear
	keep if stname == "`sta'"
	
	tw ///
		(line rel_unemployment gunemployment date, sort) ///
		(lpoly gunemployment date), ///
		graphregion(color(white)) plotregion(color(white)) ///
		legend(label(1 "Relative Unemployment") label(2 "Relative Searches for 'Unemployment'") label(3 "Smoothed Searches")) ///
		title("`sta'", size(large))
		graph export "$images/`sta'_unemploymentScatter.png", replace height(250) width(357)
}


cd "$images"
putpdf begin
putpdf paragraph, font("Garamond",20) halign(center)

foreach sta of local states{
	putpdf paragraph
	putpdf image "$images/`sta'_unemploymentScatter.png"	
}
putpdf save "$images/Controls.pdf", replace


*Erases all local images
foreach sta of local states{
	erase  "$images/`sta'_unemploymentScatter.png"
		
}
