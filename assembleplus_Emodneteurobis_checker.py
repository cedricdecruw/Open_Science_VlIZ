#!/usr/bin/env python
#script made by Decruw Cedric
import urllib.request, json, time
import xlsxwriter
import csv
from collections import Counter
import re
'''
=> assembleplus_Emodneteurobis_checker.py:
        * purpose      : To check if the datasets that are present in Assemble+ are also present in Emodnet or eurobis.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : textfile named info_eurobis_emodnet_assembleplus.txt containing 3 fields
        * Author       : Decruw Cedric
        * DOC          : Wednesday, ‎July ‎10, ‎2019, ‏‎1:25:49 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Assemble+
'''

#config
f= open("C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\info_eurobis_emodnet_assembleplus.txt","w+")
f.write("DasID,present EurOBIS,present EMODNET")
############################
DasIDs = []
superiorrecord = []

with urllib.request.urlopen("http://www.assembleplus.eu//information-system?module=dataset&show=json&count=2000") as url:
    data = json.loads(url.read().decode())
    for archive in data:
        DasIDs.append(archive["DasID"])
    print(len(DasIDs))
    

for ids in DasIDs:
    with urllib.request.urlopen("http://www.assembleplus.eu//information-system?module=dataset&show=json&dasid="+str(ids)) as url:
        data = json.loads(url.read().decode())
        #variables info
        institute=[]
        eurobis="No"
        emodnet="No"
        for spcol in data["spcols"]:
            institute.append(spcol["SpName"])
        
        #do test for eurobis and emodnet
        for i in institute:
            if "EurOBIS" in i:
                eurobis="yes"
            if "EMODNET" in i:
                emodnet="yes"
        
        #make file for info
        f.write(str(ids)+","+eurobis+","+emodnet)
        print(str(ids)+","+eurobis+","+emodnet)
        time.sleep(0.5)
f.close()
        