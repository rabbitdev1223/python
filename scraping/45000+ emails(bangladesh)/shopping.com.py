import gzip
import urllib.request
import re

file1 = open("myfile.txt","w")
request = urllib.request.Request(
    #"https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=D&fsrc=16",
    "https://www.jobbank.gc.ca/jobsearch",
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

#first extracting 25 emails========================
rx = re.compile(r'a href="(/jobsearch/jobposting/[^\"]*)')
urls = rx.findall(str(contents))

for url in urls:
    count += 1
    print(url)
    # print("https://www.jobbank.gc.ca" + url + ":" + str(count))    
    request = urllib.request.Request(
        "https://www.jobbank.gc.ca" + url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
            "cookie":''.join(cookie)
            
        })
    response = urllib.request.urlopen(request)    
    gzipFile = gzip.GzipFile(fileobj=response)
    contents = gzipFile.read()
    
    rx = re.compile(r'<button type="button" data-jbfejobid="([\d]*)" id="applynowbutton"')
    jbfejobid = rx.findall(str(contents))
    if (len(jbfejobid) == 0):
        continue;

    params = {    
        "seekeractivity:jobid": jbfejobid[0],
        "seekeractivity_SUBMIT": "1",
        "javax.faces.ViewState": "stateless",
        "javax.faces.behavior.event": "action",
        "jbfeJobId": jbfejobid[0],
        "action": "applynowbutton",
        "javax.faces.partial.event": "click",
        "javax.faces.source": "seekeractivity",
        "javax.faces.partial.ajax": "true",
        "javax.faces.partial.execute": "jobid",
        "javax.faces.partial.render": "applynow",
        "seekeractivity": "seekeractivity"
    }    
        
    query_string = urllib.parse.urlencode( params )    
    data = query_string.encode( "utf-8" )    
    
    request = urllib.request.Request(
        "https://www.jobbank.gc.ca" + url,
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
            "cookie":''.join(cookie),
            "Faces-Request":"partial/ajax",
            
        })
    response = urllib.request.urlopen(request,data)   
    #print(response. info()) 
    gzipFile = gzip.GzipFile(fileobj=response)
    contents = gzipFile.read()

    
    rx = re.compile(r'<a href="mailto:([^\"]*)')
    emails = rx.findall(str(contents))
        
    if len(emails) == 1:
        print(str(count) +  ":" + emails[0] )
        file1.write(emails[0] + ","+ "\n")
#================================================    
#    
# print(cookie);
count = 25
#===============load more===================================
while(count < 50000):
    
    request = urllib.request.Request(
        "https://www.jobbank.gc.ca/jobsearch/job_search_loader.xhtml",
        headers={
            "Accept-Encoding": "gzip",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
            "cookie":''.join(cookie)
        })
    response = urllib.request.urlopen(request)

    gzipFile = gzip.GzipFile(fileobj=response)
    contents = gzipFile.read()

    rx = re.compile(r'a href="(/jobsearch/jobposting/[^\"]*)')
    urls = rx.findall(str(contents))

    for url in urls:
        count += 1
        print(url)
        # print("https://www.jobbank.gc.ca" + url + ":" + str(count))    
        request = urllib.request.Request(
            "https://www.jobbank.gc.ca" + url,
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
                "cookie":''.join(cookie)
                
            })
        response = urllib.request.urlopen(request)    
        gzipFile = gzip.GzipFile(fileobj=response)
        contents = gzipFile.read()
        
        rx = re.compile(r'<button type="button" data-jbfejobid="([\d]*)" id="applynowbutton"')
        jbfejobid = rx.findall(str(contents))
        if (len(jbfejobid) == 0):
        	continue;
       
        params = {    
            "seekeractivity:jobid": jbfejobid[0],
            "seekeractivity_SUBMIT": "1",
            "javax.faces.ViewState": "stateless",
            "javax.faces.behavior.event": "action",
            "jbfeJobId": jbfejobid[0],
            "action": "applynowbutton",
            "javax.faces.partial.event": "click",
            "javax.faces.source": "seekeractivity",
            "javax.faces.partial.ajax": "true",
            "javax.faces.partial.execute": "jobid",
            "javax.faces.partial.render": "applynow",
            "seekeractivity": "seekeractivity"
        }    
            
        query_string = urllib.parse.urlencode( params )    
        data = query_string.encode( "utf-8" )    
       
        request = urllib.request.Request(
            "https://www.jobbank.gc.ca" + url,
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36", 
                "cookie":''.join(cookie),
                "Faces-Request":"partial/ajax",
                
            })
        response = urllib.request.urlopen(request,data)   
        #print(response. info()) 
        gzipFile = gzip.GzipFile(fileobj=response)
        contents = gzipFile.read()

        
        rx = re.compile(r'<a href="mailto:([^\"]*)')
        emails = rx.findall(str(contents))
          
        if len(emails) == 1:
            print(str(count) +  ":" + emails[0] )
            file1.write(emails[0] + "," + "\n")

file1.close()    