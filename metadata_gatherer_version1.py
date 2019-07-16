#!/usr/bin/env python
# -*- coding: utf-8 -*-
#script by decruw cedric for Metadata Gathering
import csv
import requests
import urllib.request ,json
import re
import xlsxwriter
import os
import time
import numpy as np

#logfile for the screening of the data
logfolder = "C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\"
f= open(logfolder+"logfile.txt","w+")
#http://www.assembleplus.eu/information-system?module=dataset&show=json
#http://www.vliz.be/en/imis?module=dataset&show=xml&spcolid=27&count=1000
#http://www.assembleplus.eu/information-system?module=dataset&show=json&dasid=596
#url where I get the data from
#get all the number sfrom the searchurl /json file kek
DasIDnumbers=[]
with urllib.request.urlopen("http://www.assembleplus.eu/information-system?module=dataset&show=json&count=10000") as url:
    data = json.loads(url.read().decode())
    #print(json.dumps(data, indent=4, sort_keys=True))
    i=0
    for archives in data:
        i+=1
        DasIDnumbers.append(archives["DasID"]) 
    print(i)
    for num in DasIDnumbers:
        print(num)




url = 'http://www.assembleplus.eu/information-system?module=dataset&show=json&dasid=666'
types=["json","xml","eml","rss"]
types=["json"] #not neccesary to rum everything fro datacheck if one is present then all are present on the web 
r = requests.head(url)
r.status_code
print(r.status_code)
i=0
for i in DasIDnumbers:
    for typ in types:
        try:
            with urllib.request.urlopen("http://www.assembleplus.eu/information-system?module=dataset&show="+typ+"&dasid="+str(i)) as url:
                if typ == "json":
                        data = json.loads(url.read().decode())
                        #print(json.dumps(data, indent=4, sort_keys=True))
                        evaluation = data["dasthemes"]
                        keywords = data["keywords"]
                        print(evaluation)
                        print(keywords)                  
        except:
            f.write("No data found for asid {} format {} \n".format(i,typ))
    i+=1
    time.sleep(1)


"""
try:
  with urllib.request.urlopen("http://www.assembleplus.eu/information-system?module=dataset&show=json&dasid=133") as url:
        data = json.loads(url.read().decode())
        print(json.dumps(data, indent=4, sort_keys=True))
        evaluation = data["dasthemes"]
        keywords = data["keywords"]
except:
  f.write("No data found for record {} format {}".format(,))
  

with urllib.request.urlopen("http://www.assembleplus.eu/information-system?module=dataset&show=json&dasid=133") as url:
        data = json.loads(url.read().decode())
        print(json.dumps(data, indent=4, sort_keys=True))
        evaluation = data["dasthemes"]
        keywords = data["keywords"]
"""       
