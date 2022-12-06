

/// 1. Create loop for Python and path

*TableNumber goes in the quote
local Name_ACS "#INSERT TABLE NAME"
local file "`Name_ACS'_2019_5yr_ACS.dta"

macro list

/// 2. Python code to get API
python:

from sfi import Macro
import requests
import pandas as pd
import json

ACS1 = Macro.getLocal("Name_ACS")

api = 'https://api.census.gov/data/2019/acs/acs5?get'
ACS_table = "=NAME," + "group(" + ACS1 + ")"
ACS_geo = "&for=tract:*&in=state:01&key="
key = "0945e6749213d7063a7ac5495656308cad69476d"

url = api + ACS_table + ACS_geo + key

print(url)

data = requests.get(url).json()

ACS_df = pd.read_json(json.dumps(data))

ACS_df.to_stata(ACS1+'_2019_5yr_ACS.dta', version=118)

end

/// 2. Load File
use `file', clear


/// 3. Make Row 1 the variable names

drop index
foreach var of varlist * {
    local newname = strtoname(`var'[1])
capture rename `var' `newname'        
}

drop in 1

capture mkdir "Census_Api"

cd "Census_Api"

save `file', replace

