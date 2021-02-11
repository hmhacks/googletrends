
import delimited "/..Data/allSearchTerms.csv", encoding(UTF-8) clear
gen time = date(date, "YMD")
format time %td
drop date v1

global regressors = "brownierecipe candycrush cheapgym coursera ebay googleflights harrypotter howtobakebread mensunderwear onlinemasters spidersolitaire"
*xtset

* Model
reg unemployment $regressors i.state time, robust
