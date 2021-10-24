import gzip
import urllib.request

request = urllib.request.Request(
    "http://conrad.com",
    headers={
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11", 
    })
response = urllib.request.urlopen(request)
gzipFile = gzip.GzipFile(fileobj=response)
print(gzipFile.read())