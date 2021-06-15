// cap ssc install lassopack
// cap ssc install pdslasso
// cap ssc install putexcel
/*
Generates elasticnetBetas.xlsx.

Demo for model regularization.



*/

clear all

import delimited "/Users/henrymanley/Desktop/Research/googletrends/Data/workingData.csv", clear
drop _me stname
tempfile data
save `data'


	mata
	void convert(){
		ebic = st_matrix("r(ebic)")
		M = colmin(ebic)
		st_numscalar("r(Stmin)", M)
	}
	end


global terms = "vodka jobs lottery haircut spidersolitaire blooddrive brownierecipe xbox linkedin candycrush omegle harvard jobsnearme pornhub googleflights resumetemplate ebay gunemployment slutload calvinklein"


levelsof fips, local(states)
*21 == dim == number of covariates
// loc states = 1
mat accum = J(1, 23, 0)
foreach sta of local states {

	use `data', clear
	qui keep if fips == `sta'
	qui lasso2 unemployment_rate $terms, ols alpha(0.1) long

	mat rSq = r(rsq)
	mat Betas = r(betas)
	scalar dim = `=colsof(Betas)'
	mata: convert()
	scalar thresh = r(Stmin)

	loc count = 1
	forval i = 1/`r(lcount)'{
		if r(ebic)[`i', 1] == thresh {

			continue, break
		}
		local count = `count' + 1
	}

	scalar rSq = rSq[`count', 1]
	mat betas = Betas[`count', 1..dim]
	mat accum = (accum \ `sta', betas, rSq)
	mat colnames accum ="State" $terms "Constant" "r2"
// 	lasso2, lic(ebic)
}

putexcel set "/Users/henrymanley/Desktop/Research/googletrends/Data/elasticnetBetas.xlsx", sheet("1") replace
putexcel A1=matrix(accum), colnames
