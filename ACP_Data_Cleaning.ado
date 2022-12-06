/// 1. ACP Cleaning Program 

program ACP_Data_Cleaning
	args zips time 
	tempvar Zero Zipcode_TV Datamonth_Seq Monthtest
	
/// 1. Generating Proper Zipcode String 
gen `Zero' = "0" if ZipCode < 10000
	replace `Zero' = "00" if ZipCode < 1000

tostring ZipCode, gen(`Zipcode_TV') 

egen Zipcode = concat(`Zero' `Zipcode_TV')

/// 2. Keeping the most up to date data month 

gsort + Zipcode - DataMonth 

by Zipcode:gen `Datamonth_Seq' = _n
		drop if `Datamonth_Seq'>1

		gen `Monthtest' = month(DataMonth) 
			

/// 3. Saving the file
local path = "C:\Users\SAnderson\Documents\Working Folder\Support\Rural\Elizabeth Lima\Enrolle_Data"
local file = "ACP_Claim_Data"
local Month = `Monthtest'

save  "`path'/`file'_`Month'.dta", replace 
	
	
end 