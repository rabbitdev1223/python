import gzip
import urllib.request
import re


request = urllib.request.Request(
    #"https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=D&fsrc=16",
    "https://https://www.dhl.com",
    headers={
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 

    })
    
response = urllib.request.urlopen(request)

cookie = response.info().get_all('Set-Cookie')

gzipFile = gzip.GzipFile(fileobj=response)
contents = gzipFile.read()
cookie = response.info().get_all('Set-Cookie')
# print(cookie);
count = 0
print(cookie)
# request = urllib.request.Request(
#         "https://www.dhl.com/utapi?trackingNumber=JJD140583585819&language=en",
#         headers={
#             "Accept-Encoding": "gzip",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
#             "cookie":''.join(cookie)
            
#         })
# response = urllib.request.urlopen(request)    
# gzipFile = gzip.GzipFile(fileobj=response)
# contents = gzipFile.read()
# print(contents)