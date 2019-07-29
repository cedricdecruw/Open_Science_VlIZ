#!/usr/bin/env python
# -*- coding: utf-8 -*-
#script by decruw cedric for FAIR DATABASE Analysis
from bs4 import BeautifulSoup
import csv
import requests
import urllib.request ,json
import re
import xlsxwriter
import os
import time
import numpy as np

'''
=> Fairtest.py
        * purpose      : To analyse and automise the test of the metadata from assemble+ to determine if the metadata is fair.
        * input        : no fileinput required , info is gathered from url-response.
        * output       : excelsheet named Fairtest_data_database_NAME-OF-DATASET.xlsx
        * Author       : Decruw Cedric
        * DOC          : ‎Monday, ‎July ‎1, ‎2019, ‏‎3:29:29 PM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : WP2
'''

#config

FAIRCSV = "C:\\Users\\cedricd\\Downloads\\Fairchecking.csv"
jsonfolder = "C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_json\\"
#make excelsheet
#summary : archive , success, failed, percentage (total on the bottom)
#extensive : archive, url, succes/failed, metric, info fail
workbook = xlsxwriter.Workbook('FAIRcheck.xlsx')
worksheetsum = workbook.add_worksheet("summary")
worksheetnor = workbook.add_worksheet("extensive")
#headers of worksheets
worksheetnor.write('A1',"archive")
worksheetnor.write('B1',"url")
worksheetnor.write('C1',"succ/fail")
worksheetnor.write('D1',"metric")
worksheetnor.write('E1',"Info_fail")

worksheetsum.write('A1',"archive")
worksheetsum.write('B1',"success")
worksheetsum.write('C1',"failed")
worksheetsum.write('D1',"percentage succes")
#function

def evaluatorus(evallo,headmetric,numbur):
    global excelsheet1
    global excelsheet2
    global totalfailure
    global totalsucceses
    global F1U,F1I,F1D,F2S,F2G,F3D,F3M,F4S,A1D,A1M,A1DA,A1MA,A2M,I1MW,I1MS,I1DW,I1DS,I2MW,I2MS,I3MR,R1LS,R1LW
    with urllib.request.urlopen("https://ejp-evaluator.appspot.com/FAIR_Evaluator/evaluations/"+str(evallo)+".json") as url:
        data = json.loads(url.read().decode())
        if headmetric == "F":
            f= open(jsonfolder+"F"+str(numbur)+".json","w+")
            f.write(json.dumps(data))
            f.close
        if headmetric == "A":
            f= open(jsonfolder+"A"+str(numbur)+".json","w+")
            f.write(json.dumps(data))
            f.close
        if headmetric == "I":
            f= open(jsonfolder+"I"+str(numbur)+".json","w+")
            f.write(json.dumps(data))
            f.close
        if headmetric == "R":
            f= open(jsonfolder+"R"+str(numbur)+".json","w+")
            f.write(json.dumps(data))
            f.close
        
       
        #print(json.dumps(data, indent=4, sort_keys=True))
        evaluation = data["evaluationResult"]
        #new var 
        successes = 0
        failures = 0 
        nowfail = 2 
        delimiters = "FAIR_Evaluator/metrics"
        stn_split = re.split(delimiters,evaluation)
        z=1
        summartrow=[] #to put data from summary in 
        for splits in stn_split:
            currentrow=[] #iedere keer resetten
            if "FAILURE" in splits:
                failures+=1
                nowfail = 1
                #print(splits)
                #info about the faillure
                failsplit = re.split("FAILURE:",splits)
                info = re.split("metric", failsplit[1])
                #print("FAILURE : {}metric".format(info[0]))
                
            if "SUCCESS" in splits:
                successes+=1
                nowfail = 0
                successsplit = re.split("SUCCESS:",splits)
                info = re.split("metric", successsplit[1])
                #print("SUCCESS : {}metric".format(info[0]))
            #principle F1 ,R1.2 etc
            #info about the metrics can be found via this url https://ejp-evaluator.appspot.com/FAIR_Evaluator/metrics
            if headmetric == "F":
                if z == 1:
                    metric = "F1: FAIR Metrics Gen2- Unique Identifier"
                    
                    if "SUCCESS" in splits:
                        F1U+=1
                    
                if z == 2:
                    metric = "F1: FAIR Metrics Gen2 - Identifier Persistence"
                    
                    if "SUCCESS" in splits:
                        F1I+=1
                        
                if z == 3:
                    metric = "F1: FAIR Metrics Gen2 - Data Identifier Persistence"
                    
                    if "SUCCESS" in splits:
                        F1D+=1 
                if z == 4:
                    metric = "F2: FAIR Metrics Gen2 - Structured Metadata"
                                      
                    if "SUCCESS" in splits:
                        F2S+=1
                        
                if z == 5:
                    metric = "F2: FAIR Metrics Gen2 - Grounded Metadata"
                     
                    if "SUCCESS" in splits:
                        F2G+=1 
                    
                if z == 6:
                    metric = "F3: FAIR Metrics Gen2 - Data Identifier Explicitly In Metadata"
                                
                    if "SUCCESS" in splits:
                        F3D+=1 
                    
                if z == 7:
                    metric = "F3: FAIR Metrics Gen2- Metadata Identifier Explicitly In Metadata"
                       
                    if "SUCCESS" in splits:
                        F3M+=1
                    
                if z == 8:
                    metric = "F4: FAIR Metrics Gen2 - Searchable in major search engine"  
                    
                    if "SUCCESS" in splits:
                        F4S+=1
                      
            if headmetric == "A":
                if z == 1:
                    metric = "A1.1: FAIR Metrics Gen2 - Uses open free protocol for data retrieval"
                       
                    if "SUCCESS" in splits:
                        A1D+=1 
                     
                if z == 2:
                    metric = "A1.1: FAIR Metrics Gen2 - Uses open free protocol for metadata retrieval"
                     
                    if "SUCCESS" in splits:
                        A1M+=1 
                     
                if z == 3:
                    metric = "A1.2: FAIR Metrics Gen2 - Data authentication and authorization"
                    
                    if "SUCCESS" in splits:
                        A1DA+=1
                     
                if z == 4:
                    metric = "A1.2: FAIR Metrics Gen2 - Metadata authentication and authorization"
                    
                    if "SUCCESS" in splits:
                        A1MA+=1
                     
                if z == 5:
                    metric = "A2: FAIR Metrics Gen2 - Metadata Persistence"
                    
                    if "SUCCESS" in splits:
                        A2M+=1
                     
            if headmetric == "I":
                if z == 1:
                    metric = "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (weak)"
                    
                    if "SUCCESS" in splits:
                        I1MW+=1
                    
                if z == 2:
                    metric = "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (strong)"
                    
                    if "SUCCESS" in splits:
                        I1MS+=1
                    
                if z == 3:
                    metric = "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (weak)"
                    
                    if "SUCCESS" in splits:
                        I1DW+=1
                    
                if z == 4:
                    metric = "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (strong)"
                    
                    if "SUCCESS" in splits:
                        I1DS+=1
                    
                if z == 5:
                    metric = "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (weak)"
                    
                    if "SUCCESS" in splits:
                        I2MW+=1
                    
                if z == 6:
                    metric = "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (strong)"
                    
                    if "SUCCESS" in splits:
                        I2MS+=1
                    
                if z == 7:
                    metric = "I3: FAIR Metrics Gen2 - Metadata contains qualified outward references)"
                    
                    if "SUCCESS" in splits:
                        I3MR+=1
                    
            if headmetric == "R":
                if z == 1:
                    metric = "R1.1: FAIR Metrics Gen2 - Metadata Includes License (strong)"
                    
                    if "SUCCESS" in splits:
                        R1LS+=1
                    
                if z == 2:
                    metric = "R1.1: FAIR Metrics Gen2 - Metadata Includes License (weak)"
                    
                    if "SUCCESS" in splits:
                        R1LW+=1
                    
            z+=1
            
            if nowfail == 0:
                print("SUCCES on metric {}".format(metric))
                #input extensive in excel
                currentrow.append(uniquedatabase[numbur])
                currentrow.append(uniqueurls[numbur])
                currentrow.append("SUCCES")
                currentrow.append(metric)
                currentrow.append("NAN")
                excelsheet2.append(currentrow)
            elif nowfail == 1:
                print("FAILED on metric {}".format(metric))
                currentrow.append(uniquedatabase[numbur])
                currentrow.append(uniqueurls[numbur])
                currentrow.append("FAILED")
                currentrow.append(metric)
                currentrow.append(info[0])
                excelsheet2.append(currentrow)
            else:
                print("NO RESULT GIVEN")
            
            
        
        print("{} ,{}".format(successes,(failures+successes)))
        totalfailure+=failures
        totalsucceses+=successes
        #input summary in excel
        if headmetric == "F":
            summartrow.extend([uniquedatabase[numbur] + " F",successes,failures,((successes/(successes+failures))*100)])
        elif headmetric == "A":
            summartrow.extend([uniquedatabase[numbur] + " A",successes,failures,((successes/(successes+failures))*100)])
        elif headmetric == "I":
            summartrow.extend([uniquedatabase[numbur] + " I",successes,failures,((successes/(successes+failures))*100)])
        elif headmetric == "R":
            summartrow.extend([uniquedatabase[numbur] + " R",successes,failures,((successes/(successes+failures))*100)])
        
        
        
    #appending to excelsheets
    excelsheet1.append(summartrow)
    
    #returning variables
    return excelsheet1,excelsheet2,totalfailure,totalsucceses,F1U,F1I,F1D,F2S,F2G,F3D,F3M,F4S,A1D,A1M,A1DA,A1MA,A2M,I1MW,I1MS,I1DW,I1DS,I2MW,I2MS,I3MR,R1LS,R1LW


        

excelsheet1=[] #imortqnt
excelsheet2=[]
NameDatabase = []
URLS=[]
F=[]
A=[]
I=[]
R=[]
totalsucceses = 0
totalfailure = 0
#vars of the metrics 
#findable
F1U=0
F1I=0
F1D=0
F2S=0
F2G=0
F3D=0
F3M=0
F4S=0
#adaptable
A1D=0
A1M=0
A1DA=0
A1MA=0
A2M=0
#interoperable
I1MW=0
I1MS=0
I1DW=0
I1DS=0
I2MW=0
I2MS=0
I3MR=0
#reproducible
R1LS=0
R1LW=0


#kolom3 = evalnumber , kolom5 = letter fair
#get data from csv-file
with open(FAIRCSV) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if row[4] == "F":
                F.append(row[2])
            if row[4] == "A":
                A.append(row[2])
            if row[4] == "I":
                I.append(row[2])
            if row[4] == "R":
                R.append(row[2])
            
            NameDatabase.append(row[1])
            URLS.append(row[3])
            line_count += 1
    print(f'Processed {line_count} lines.')


#different for´s for all the letters in fair

uniquedatabase = np.unique(NameDatabase)
uniqueurls = np.unique(URLS)


#little test
print(len(uniquedatabase))




i=1
while i <= 4:
    if i == 1:
        headmetric = "F"
        b=0
        for Fs in F:
            evaluatorus(Fs,headmetric,b)  
            b+=1  
            time.sleep(1)
        #create data that takes every identifier and performs analysis on it 
               
    if i == 2:
        headmetric = "A"
        b=0
        for As in A:
            evaluatorus(As,headmetric,b)
            b+=1  
            time.sleep(1) 
    if i == 3:
        headmetric = "I"
        b=0
        for Is in I:
            evaluatorus(Is,headmetric,b)
            b+=1  
            time.sleep(1) 
    if i == 4:
        headmetric = "R"
        b=0
        for Rs in R:
            evaluatorus(Rs,headmetric,b)
            b+=1   
            time.sleep(1)
    i+=1

#adding al values to excel
row = 1
col = 0
for archive, success, failed, percentage in (excelsheet1):
     worksheetsum.write(row, col,     archive)
     worksheetsum.write(row, col + 1, success)
     worksheetsum.write(row, col + 2, failed)
     worksheetsum.write(row, col + 3, percentage)
     row += 1
#add total sum to worksheetsum
worksheetsum.write(row, col,     "TOTAL")
worksheetsum.write(row, col + 1, totalsucceses)
worksheetsum.write(row, col + 2, totalfailure)
worksheetsum.write(row, col + 3, ((totalsucceses/(totalsucceses+totalfailure))*100))
row = 1
for archive, url, sucfail, metric, info in (excelsheet2):
     worksheetnor.write(row, col,     archive)
     worksheetnor.write(row, col + 1, url)
     worksheetnor.write(row, col + 2, sucfail)
     worksheetnor.write(row, col + 3, metric)
     worksheetnor.write(row, col + 4, info)
     row += 1

#graphing info
#after all info add shart (on second thought not really possible unless I know how many unique requests there are)
chart1 = workbook.add_chart({'type': 'pie'})
chart1.add_series({
    'name':       'Pie succes/failure data',
    'categories': '=summary!$B$1:$C$1',
    'values':     '=summary!$B$'+str((len(uniquedatabase)*4))+':$C$'+str((len(uniquedatabase)*4)), #normaal +1 maar +3 omdat unique niet toekomt
    'points': [
        {'fill': {'color': '#5AFF10'}},
        {'fill': {'color': '#FE110E'}},
    ],
})
# Add a title.
chart1.set_title({'name': 'Succes-rate FAIR-test summary'})
#style
chart1.set_style(10)
#insert 
worksheetsum.insert_chart('E1', chart1, {'x_offset': 25, 'y_offset': 10})


#graphs of the more in deph info
#get info from all variables
#findable
FF1U=len(uniquedatabase)-F1U
FF1I=len(uniquedatabase)-F1I
FF1D=len(uniquedatabase)-F1D
FF2S=len(uniquedatabase)-F2S
FF2G=len(uniquedatabase)-F2G
FF3D=len(uniquedatabase)-F3D
FF3M=len(uniquedatabase)-F3M
FF4S=len(uniquedatabase)-F4S
#adaptable
FA1D=len(uniquedatabase)-A1D
FA1M=len(uniquedatabase)-A1M
FA1DA=len(uniquedatabase)-A1DA
FA1MA=len(uniquedatabase)-A1MA
FA2M=len(uniquedatabase)-A2M
#interoperable
FI1MW=len(uniquedatabase)-I1MW
FI1MS=len(uniquedatabase)-I1MS
FI1DW=len(uniquedatabase)-I1DW
FI1DS=len(uniquedatabase)-I1DS
FI2MW=len(uniquedatabase)-I2MW
FI2MS=len(uniquedatabase)-I2MS
FI3MR=len(uniquedatabase)-I3MR
#reproducible
FR1LS=len(uniquedatabase)-R1LS
FR1LW=len(uniquedatabase)-R1LW

#put everything in an excelsheet for graph making 
worksheetgraphs = workbook.add_worksheet("graph")
worksheetgraphs.write('A1',"metric")
worksheetgraphs.write('B1',"short-metric")
worksheetgraphs.write('C1',"fail")
worksheetgraphs.write('D1',"succes")
summarymetrics=[]
succ=[F1U,F1I,F1D,F2S,F2G,F3D,F3M,F4S,A1D,A1M,A1DA,A1MA,A2M,I1MW,I1MS,I1DW,I1DS,I2MW,I2MS,I3MR,R1LS,R1LW]
fail=[FF1U,FF1I,FF1D,FF2S,FF2G,FF3D,FF3M,FF4S,FA1D,FA1M,FA1DA,FA1MA,FA2M,FI1MW,FI1MS,FI1DW,FI1DS,FI2MW,FI2MS,FI3MR,FR1LS,FR1LW]
metricss=["F1: FAIR Metrics Gen2- Unique Identifier",
          "F1: FAIR Metrics Gen2 - Identifier Persistence",
          "F1: FAIR Metrics Gen2 - Data Identifier Persistence",
          "F2: FAIR Metrics Gen2 - Structured Metadata",
          "F2: FAIR Metrics Gen2 - Grounded Metadata",
          "F3: FAIR Metrics Gen2 - Data Identifier Explicitly In Metadata",
          "F3: FAIR Metrics Gen2- Metadata Identifier Explicitly In Metadata",
          "F4: FAIR Metrics Gen2 - Searchable in major search engine",
          "A1.1: FAIR Metrics Gen2 - Uses open free protocol for data retrieval",
          "A1.1: FAIR Metrics Gen2 - Uses open free protocol for metadata retrieval",
          "A1.2: FAIR Metrics Gen2 - Data authentication and authorization",
          "A1.2: FAIR Metrics Gen2 - Metadata authentication and authorization",
          "A2: FAIR Metrics Gen2 - Metadata Persistence",
          "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (weak)",
          "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (strong)",
          "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (weak)",
          "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (strong)",
          "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (weak)",
          "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (strong)",
          "I3: FAIR Metrics Gen2 - Metadata contains qualified outward references)",
          "R1.1: FAIR Metrics Gen2 - Metadata Includes License (strong)",
          "R1.1: FAIR Metrics Gen2 - Metadata Includes License (weak)"  
]
short_metric=["F1U","F1I","F1D","F2S","F2G","F3D","F3M","F4S","A1D","A1M","A1DA","A1MA","A2M","I1MW","I1MS","I1DW","I1DS","I2MW","I2MS","I3MR","R1LS","R1LW"]
i=0
while i < 22:
    currentrow=[]
    currentrow.extend([metricss[i],short_metric[i],fail[i],succ[i]]) 
    summarymetrics.append(currentrow)
    i+=1
   
#adapt to new rules 
row = 1
for metric, smetric, fail, succ in (summarymetrics):
     worksheetgraphs.write(row, col,     metric)
     worksheetgraphs.write(row, col + 1,   smetric)
     worksheetgraphs.write(row, col + 2, fail)
     worksheetgraphs.write(row, col + 3, succ)
     row += 1

#implement shart
chart3 = workbook.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})
chart3.add_series({
    'name':       '=graph!$C$1',
    'categories': '=graph!$B$2:$B$23',
    'values':     '=graph!$C$2:$C$23',
})
chart3.add_series({
    'name':       '=graph!$D$1',
    'categories': '=graph!$B$2:$B$23',
    'values':     '=graph!$D$2:$D$23',
})
# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent failed/succeeded'})
chart3.set_x_axis({'name': 'failed/succeeded (%)'})
chart3.set_y_axis({'name': 'short-metric'})
# Set an Excel chart style.
chart3.set_style(2)
# Insert the chart into the worksheet (with an offset).
worksheetgraphs.insert_chart('F5', chart3, {'x_offset': 30, 'y_offset': 80})
workbook.close()