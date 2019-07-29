#!/usr/bin/env python
#script made by Decruw Cedric
import urllib.request, json, time, csv
import requests
import numpy 
import xlsxwriter

'''
=> tussenscript.py
        * purpose      : Dumpfile for code.
        * input        : no fileinput required.
        * output       : no output.
        * Author       : Decruw Cedric
        * DOC          : ‎Friday, ‎July ‎5, ‎2019, ‏‎13:52:04 AM
        * Requirements : No other scripts are required to have ran before running this script.
        * PCF          : Others
'''

nametests = ["F1: FAIR Metrics Gen2- Unique Identifier","F1: FAIR Metrics Gen2 - Identifier Persistence","F1: FAIR Metrics Gen2 - Data Identifier Persistence",
             "F2: FAIR Metrics Gen2 - Structured Metadata","F2: FAIR Metrics Gen2 - Grounded Metadata","F3: FAIR Metrics Gen2 - Data Identifier Explicitly In Metadata",
             "F3: FAIR Metrics Gen2- Metadata Identifier Explicitly In Metadata","F4: FAIR Metrics Gen2 - Searchable in major search engine",
             "A1.1: FAIR Metrics Gen2 - Uses open free protocol for data retrieval","A1.1: FAIR Metrics Gen2 - Uses open free protocol for metadata retrieval",
             "A1.2: FAIR Metrics Gen2 - Data authentication and authorization","A1.2: FAIR Metrics Gen2 - Metadata authentication and authorization",
             "A2: FAIR Metrics Gen2 - Metadata Persistence","I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (weak)",
             "I1: FAIR Metrics Gen2 - Metadata Knowledge Representation Language (strong)","I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (weak)",
             "I1: FAIR Metrics Gen2 - Data Knowledge Representation Language (strong)","I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (weak)",
             "I2: FAIR Metrics Gen2 - Metadata uses FAIR vocabularies (strong)","I3: FAIR Metrics Gen2 - Metadata contains qualified outward references)",
             "R1.1: FAIR Metrics Gen2 - Metadata Includes License (strong)","R1.1: FAIR Metrics Gen2 - Metadata Includes License (weak)"]
short_metric=["F1U","F1I","F1D","F2S","F2G","F3D","F3M","F4S","A1D","A1M","A1DA","A1MA","A2M","I1MW","I1MS","I1DW","I1DS","I2MW","I2MS","I3MR","R1LS","R1LW"]
savefolder="C:\\Users\\cedricd\\Documents\\Pre_upload_folder\\temp_files_screening_databases\\"
counttestdictionary={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0,21:0}
with open(savefolder+"jsondumpfolder\\info_jsondumpfile_xml_dataset6015.txt") as f:
    data = json.load(f)


    results = data["evaluationResult"]
    testdataresults=results.split("https://w3id.org/FAIR_Evaluator/metrics/")
    #analyse the chunks
    #array of results
    resultsdata = []
    test = 0
    succestest=0
    for result in testdataresults:
        #extract all data 

        if "@id" in result:
            rowdata=[]
            testname=nametests[test]
            valueresults = result.split("@value")
            for values in valueresults:
                print(values[0:10])
                #do tests for getting data
                if '":"0"' in values[0:10]:
                    #print("0 added")
                    test+=1   
                if '":"1"' in values[0:10]:
                    #print("1 added")
                    counttestdictionary[test]= counttestdictionary[test]+1
                    succestest+=1
                    test+=1
    
    print(test)
    for x,y in counttestdictionary.items():
        print(x,y)
    print(succestest)