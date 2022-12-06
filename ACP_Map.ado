
program ACP_Map
	args TotalSubscribers
	tempvar _mergeACP

/// 1. Merge Files 

 
merge 1:1 Zipcode using "C:\Users\SAnderson\Documents\Working Folder\Support\Rural\Elizabeth Lima\B25010_HH_Avg\Derived_Household_Income_Brackets_Basefile_9.6.2022.dta", gen(`_mergeACP')

	

gen Eligible_Prop = TotalSubscribers/Eligibility
		gen Eligible_Prop2 = Eligible_Prop
	
		/// Rule 1: If over 1, change to 1.01
		replace Eligible_Prop2 = 1.01 if Eligible_Prop>1
		
	/// Rule 2: If Total Subscribers or Census Eligibility is missing, equals 999
		replace Eligible_Prop2 = 999 if TotalSubscribers==. | Eligibility==.
		
	/// Rule 3: If total subscribers is missing and there are income-eligible households, then set to 0
		replace Eligible_Prop2 = 0 if Eligible_Prop==. & TotalSubscribers==. & Eligibility>0
	
	/// Rule 3: Total Subscribers is greater than 0 and  Eligibility is 0, then 1.01
		replace Eligible_Prop2=1.01 if TotalSubscribers>0 & TotalSubscribers!=. & Eligibility==0

	/// Generate Percentage Variable
		gen Enrolle_Perc = Eligible_Prop2
			replace Enrolle_Perc = Eligible_Prop2 * 100 if Eligible_Prop2!=999 
			gsort - Enrolle_Perc

local path = "C:\Users\SAnderson\Documents\Working Folder\Support\Rural\Elizabeth Lima\Enrolle_Data"
local file = "ACP_Claims_JoinedZipcode"
local today = c(current_date)

tostring Enrolle_Perc, gen(Enrollt) force


save "`path'/`file'_`today'.dta" , replace 

rename Eligibility Eligible
rename Enrolle_Perc Enr_Prop
rename TotalSubscribers Subscribe


export dbase Zipcode Eligible Enr_Prop Enrollt Subscribe using "`path'/`file'_`today'_dbf", datafmt replace

rename  Eligible Eligibility
rename  Enr_Prop Enrolle_Perc
rename  Subscribe TotalSubscribers

end 