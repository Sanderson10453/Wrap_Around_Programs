
from ast import Lambda
from dataclasses import replace
import requests
from bs4 import BeautifulSoup
import csv 

api = 'https://www.findagrave.com/memorial/search?'
name = 'firstname=&middlename=&lastname='
years = 'birthyear=&birthyearfilter=&deathyear=&deathyearfilter='
place = 'location=Yulee%2C+Nassau+County%2C+Florida%2C+United+States+of+America&locationId=city_28711'
memorialid = 'memorialid=&mcid='
linkname = 'linkedToName='
daterange = 'datefilter='
plotnum = 'orderby=r&plot='
page = 'page='
url = api + name + "&" + years + "&" + place + "&" + memorialid + "&" + linkname + "&" + daterange + "&" + plotnum + '&' + page

#url2 = "https://www.findagrave.com/memorial/search?firstname=&middlename=&lastname=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=Yulee%2C+Nassau+County%2C+Florida%2C+United+States+of+America&locationId=city_28711&memorialid=&mcid=&linkedToName=&datefilter=&orderby=r&plot=&page="

headers ={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate',
'accept-language': 'en-US,en;q=0.9',
'cache-control': 'max-age=0',
'cookie': 'preferredLanguage=en; tzo=-240; dnsDisplayed=undefined; ccpaApplies=false; signedLspa=undefined; consentSettings={"pref":true,"ga":true,"aa":true}; _sp_sampled_user=true; _pubcid=9007fa3c-309d-403c-8be6-82d593282654; _adb=a2l8w3lglfkcXGviv95t; consentUUID=d6dbd456-7ec2-4b14-a17d-b41143d81563; _admrla=2.2-03a911566ab1d53f-7e03a5f7-44ee-11ed-89de-085c0e5754d8; AMCVS_ED3301AC512D2A290A490D4C%40AdobeOrg=1; s_cc=true; _cc_id=e79436306a916453e052c8eb2519ede2; ipLoc=us; __cfruid=8be876eac81bae94003d29582bc1dbc35ed027fa-1665503732; adbrgn=US%3F%3F; _awl=2.1665503733.0.5-d41b07d2ec7fb7c1b656181246d31378-6763652d75732d6561737431-0; ccpaUUID=4dba8514-db4a-47c3-8ea2-a2d2992b0232; _gid=GA1.2.1340969650.1665503734; panoramaId_expiry=1666108534235; panoramaId=d42ab6c075948a812956cef24e9e16d53938b4ea51739301af7139e4470c0554; _ga_8218P4T90M=GS1.1.1665503734.2.0.1665503734.0.0.0; _ga=GA1.1.1046559442.1665002662; AMCV_ED3301AC512D2A290A490D4C%40AdobeOrg=1585540135%7CMCMID%7C14769305974362614120618594529978098085%7CMCAAMLH-1666108534%7C7%7CMCAAMB-1666108534%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1665510934s%7CNONE%7CMCSYNCSOP%7C411-19278%7CvVersion%7C4.4.0; __gads=ID=5a80ad8a9ad89c21-22daa8aaaad7008e:T=1665503734:S=ALNI_Mb7s7sdRPGLcYBh3VUAO31HnjHFmA; __gpi=UID=00000882ef7ef3ea:T=1665503734:RT=1665503734:S=ALNI_Mb0d5syY4AOVHq5j-FC9OzZbgG4TQ',
'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}	


params = 'firstname=&middlename=&lastname=&birthyear=&birthyearfilter=&deathyear=&deathyearfilter=&location=Nassau+County%2C+Florida%2C+United+States+of+America&locationId=county_360&memorialid=&mcid=&linkedToName=&datefilter=&orderby=r&plot=&page='



for page_no in range(1,93): 
   url_final = url + str(page_no)
   page = requests.get(url_final, headers = headers)

   #print(page)
   soup = BeautifulSoup(page.content, "html.parser")
   for x in soup.find_all():
    if len(x.get_text(strip=True)) == 0 and x.name in ['h2']:
      x.extract()
   #Getting the Names 
   grave_name = soup.find_all('h2', {'class': 'name-grave'})
   
   #Dates
   dates = soup.find_all('b', {'class':'birthDeathDates'})

   #Graveyard Name
   grave_yard = soup.find_all('button', {'role': 'link'})
   #print(grave_yard)
   
   dataset = [(x.text, y.text, z.text) for x,y,z in zip(grave_name, dates, grave_yard)]
   with open('Fernandiabeach3.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(dataset)

