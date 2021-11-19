import pandas as pd
import datetime as dt1
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import json
# import json

options = Options()
options.add_experimental_option("prefs", {
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe",options=options)
url="https://www.kayak.com/flight-trends"
driver.get (url)

content = driver.page_source
soup = BeautifulSoup(content,'html.parser')


rx = re.compile(r'"data":(\[[^\]]+\])')

matches = rx.findall(str(soup))

count = 0
data_array = [];
for match in matches:
   
    data_array.append(json.loads(match))

print(data_array[0][-1])
print(data_array[1][-1])
print(data_array[2][-1])
    
    
    
# for x in soup.find_all('script', type='text/javascript'):
    
#     if "new R9.common.seo.Highchart" in x:
#         print ("yes")
#         # rx = r'"data":[.+)\;'
#         rx = r'"data":\[.+(?=\]\,).+'
#         # rx=r'"data":\[.+?(\]\,)'
#         matches = re.findall(rx, x.text)
#         print (matches[0])
#         # break
#         # data=json.loads(matches)
#         # print (data)
#     else:
#         print ("no")