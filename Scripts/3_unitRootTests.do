/*
Henry Manley - hjm67@cornell.edu -  Last Modified 7/12/2021
*/

//  https://www.stata.com/manuals/tsdfuller.pdf
cap prog drop augDickeyFuller
prog def augDickeyFuller
  syntax varlist
  for var in `varlist'{
    dfuller `var'
  }
end
