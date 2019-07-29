#!/usr/bin/env python
#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re

'''
 => assembleplus_vliz_checker.py:
        * purpose      : To analyse the metadata from the extracted imis databases.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : textfile named metadata_vliz_checker__NAME-OF-DATASET.txt containing 5 fields
        * Author       : Decruw Cedric
        * DOC          : Wednesday, ‎July ‎10, ‎2019, ‏‎1:02:43 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Assemble+
'''
#config
insids = ["36","1878","4047","4724","6355","950","717","5204","471"]
insnames = ["VLIZ","HCMR","HCMR","HCMR","HCMR","AWI","AWI","AWI","UGENT"]
spcolids = ["951","952","950"] #make array for which i put the spcolids to see if they all are the same (all the same) "27","910","896",
namesdatabases = ["Assemblemarine","Assembleplus","EMBRC"] #"ScheldeMonitor","jerico-_next","Lifewatch",
totaal=10000
step=5000
nameolol=0

savefolder="S:\\datac\\Projects\\AssemblePlus\\NA2_DataAccess\\Development4AssemblePCollection\\"
#get dasids from the datasets
for spcolid in spcolids:  
    insnamesnumber=0 
    f= open(savefolder+"metadata_vliz_checker_"+namesdatabases[nameolol]+".txt","w+")
    f.write("DasID | Institute ID | Name linked to Institute ID | Acronyms in Dataset | RoleIDS in Dataset\n")
    for insid in insids:
        DasIDs=[]
        current=0
        while current < totaal:
            with urllib.request.urlopen("http://www.vliz.be/en/imis?module=dataset&count="+str(step)+"&show=json&start="+str(current)+"&spcolid="+str(spcolid)+"&insid="+str(insid)) as url:
                try:
                    data = json.loads(url.read().decode())
                    #print(json.dumps(data, indent=4, sort_keys=True))
                    for archive in data:
                        DasIDs.append(archive["DasID"])
                    time.sleep(1)
                    print(len(DasIDs))
                    current+=step
                except:
                    print(len(DasIDs))
                    pass
        
        #here snippet code for extractinf info 
        for ids in DasIDs:
            with urllib.request.urlopen("http://www.vliz.be/en/imis?module=dataset&show=json&dasid="+str(ids)) as url:
                acronyms=[]
                roleids=[]
                data = json.loads(url.read().decode())
                try:
                    ownership = data["ownerships"]
                except KeyError:
                    ownership = ["NA"]
                
                try:
                    for shiprecs in ownership:
                        acronyms.append(shiprecs["Acronym"])
                        roleids.append(shiprecs["RoleID"])                
                except:
                    acronyms.append("NA")
                    roleids.append("NA")
                    
                #make line
                line = str(ids)+"|"+str(insid)+"|"+insnames[insnamesnumber]+"|"+str(acronyms)+"|"+str(roleids)
                try:
                    f.write(line + "\n") 
                    print(line)
                except UnicodeEncodeError:
                    print()
            time.sleep(0.2)
        insnamesnumber+=1
    nameolol+=1       
    f.close() 
            